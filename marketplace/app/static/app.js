const SHOPPER_ID = "shopper-river";
const ADMIN_ID = "admin-stone";

const state = {
  userId: SHOPPER_ID,
  view: "shop",
  adminSection: "inventory",
  products: [],
  cart: { items: [], total_cents: 0 },
  orders: [],
  adminOrders: [],
  category: "all",
  search: "",
  checkoutKey: null,
  checkoutOutcome: null,
};

const content = document.querySelector("#app-content");
const identitySelect = document.querySelector("#identity-select");
const message = document.querySelector("#app-message");
const nav = document.querySelector("#main-nav");
const cartCount = document.querySelector("#cart-count");

const categoryInfo = {
  food: { label: "Foods", icon: "🍓" },
  stones: { label: "Stones", icon: "🪨" },
  sticks: { label: "Sticks", icon: "🪵" },
  toys: { label: "Toys", icon: "🦆" },
};

class ApiError extends Error {
  constructor(messageText, statusCode) {
    super(messageText);
    this.status = statusCode;
  }
}

async function api(path, { method = "GET", body, headers = {} } = {}) {
  const requestHeaders = new Headers(headers);
  requestHeaders.set("X-User-Id", state.userId);
  if (body !== undefined) requestHeaders.set("Content-Type", "application/json");

  const response = await fetch(path, {
    method,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const responseText = await response.text();
  let result = null;
  if (responseText) {
    try {
      result = JSON.parse(responseText);
    } catch {
      result = null;
    }
  }
  if (!response.ok) {
    throw new ApiError(
      result?.detail || `The request could not be completed (${response.status}).`,
      response.status,
    );
  }
  return result;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function money(cents) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" })
    .format(cents / 100);
}

function displayDate(value) {
  const date = new Date(`${value.replace(" ", "T")}Z`);
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString();
}

function showMessage(text, tone = "info") {
  message.textContent = text;
  message.dataset.tone = tone;
  message.hidden = false;
}

function clearMessage() {
  message.hidden = true;
  message.textContent = "";
  delete message.dataset.tone;
}

function isAdmin() {
  return state.userId === ADMIN_ID;
}

function updateNavigation() {
  nav.querySelector('[data-view="shop"]').hidden = isAdmin();
  nav.querySelector('[data-view="cart"]').hidden = isAdmin();
  nav.querySelector('[data-view="orders"]').hidden = isAdmin();
  nav.querySelector('[data-view="admin"]').hidden = !isAdmin();
  nav.querySelectorAll("[data-view]").forEach((button) => {
    const active = button.dataset.view === state.view;
    button.classList.toggle("is-active", active);
    if (active) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
  const count = state.cart.items.reduce((sum, item) => sum + item.quantity, 0);
  cartCount.textContent = String(count);
}

function productCard(product) {
  const kind = categoryInfo[product.category] || { label: product.category, icon: "🌿" };
  const outOfStock = product.stock === 0;
  return `
    <article class="product-card">
      <div class="product-art" data-kind="${escapeHtml(product.category)}" aria-hidden="true">
        <span class="product-symbol">${kind.icon}</span>
        <small>cove find</small>
      </div>
      <p class="product-category">${escapeHtml(kind.label)}</p>
      <h3>${escapeHtml(product.name)}</h3>
      <div class="product-bottom">
        <div><span class="price">${money(product.price_cents)}</span>
          <span class="stock-note">${outOfStock ? "Out of stock" : `${product.stock} in stock`}</span></div>
        <button class="button" type="button" data-action="add" data-product-id="${escapeHtml(product.id)}" ${outOfStock ? "disabled" : ""}>
          ${outOfStock ? "Unavailable" : "Add to cart"}
        </button>
      </div>
    </article>`;
}

function renderProductGrid() {
  const grid = content.querySelector("#product-grid");
  if (!grid) return;
  const term = state.search.trim().toLocaleLowerCase();
  const filtered = state.products.filter((product) => {
    const matchesCategory = state.category === "all" || product.category === state.category;
    const matchesText = !term || `${product.name} ${product.category}`.toLocaleLowerCase().includes(term);
    return matchesCategory && matchesText;
  });
  grid.innerHTML = filtered.length
    ? filtered.map(productCard).join("")
    : `<div class="empty-state" style="grid-column: 1 / -1"><strong>No finds in this nook</strong><p>Try another search or browse a different shelf.</p></div>`;
}

function renderShop() {
  content.innerHTML = `
    <section class="shop-hero" aria-labelledby="shop-title">
      <div class="hero-copy">
        <p class="eyebrow">A small shop for slow days</p>
        <h1 id="shop-title">Good things, found at an easy pace.</h1>
        <p>Berry bowls, smooth stones and little comforts, gathered for your corner of the cove.</p>
      </div>
      <div class="hero-note" aria-label="Four little shelves"><strong>04</strong><span>little shelves</span></div>
    </section>
    <div class="page-heading">
      <div><p class="eyebrow">The market</p><h2>Find your favorite</h2><p>Thoughtful everyday things, ready when you are.</p></div>
      <span class="heading-aside">${state.products.length} finds to browse</span>
    </div>
    <div class="toolbar">
      <label class="search-field"><span class="search-icon" aria-hidden="true">⌕</span><span class="visually-hidden">Search products</span>
        <input id="product-search" type="search" placeholder="Search the shelves" value="${escapeHtml(state.search)}">
      </label>
      <div class="category-filter" role="group" aria-label="Filter products by category">
        ${["all", "food", "stones", "sticks", "toys"].map((category) => {
          const label = category === "all" ? "Everything" : categoryInfo[category].label;
          return `<button type="button" class="filter-button ${state.category === category ? "is-selected" : ""}" data-category="${category}" aria-pressed="${state.category === category}">${label}</button>`;
        }).join("")}
      </div>
    </div>
    <div id="product-grid" class="product-grid" aria-live="polite"></div>`;
  renderProductGrid();
  content.querySelector("#product-search").addEventListener("input", (event) => {
    state.search = event.target.value;
    renderProductGrid();
  });
}

function renderCart() {
  const items = state.cart.items;
  const list = items.length ? `
    <div class="cart-list">
      ${items.map((item) => `
        <article class="cart-item">
          <div><p class="product-category">${escapeHtml(categoryInfo[item.category]?.label || item.category)}</p>
            <h3>${escapeHtml(item.name)}</h3><p>${money(item.price_cents)} each · ${money(item.line_total_cents)} total</p></div>
          <div class="cart-item-actions">
            <form class="quantity-form" data-form="cart-quantity" data-product-id="${escapeHtml(item.product_id)}">
              <label class="visually-hidden" for="quantity-${escapeHtml(item.product_id)}">Quantity for ${escapeHtml(item.name)}</label>
              <input id="quantity-${escapeHtml(item.product_id)}" name="quantity" type="number" min="1" step="1" value="${item.quantity}" required>
              <button class="button button-quiet" type="submit">Update</button>
            </form>
            <button class="text-button" type="button" data-action="remove" data-product-id="${escapeHtml(item.product_id)}">Remove</button>
          </div>
        </article>`).join("")}
    </div>` : `
    <div class="empty-state"><strong>Your basket is taking a rest.</strong><p>When something catches your eye, it will be waiting here.</p>
      <button class="button button-secondary" type="button" data-view="shop">Visit the market</button></div>`;
  content.innerHTML = `
    <div class="page-heading"><div><p class="eyebrow">Your basket</p><h1>A few good things.</h1><p>Prices reflect the current catalog. Stock is checked again when you check out.</p></div></div>
    ${items.length ? `<div class="cart-layout"><div>${list}</div>
      <aside class="order-summary" aria-labelledby="summary-title">
        <h2 id="summary-title">A little summary</h2>
        ${items.map((item) => `<div class="summary-row"><span>${escapeHtml(item.name)} × ${item.quantity}</span><strong>${money(item.line_total_cents)}</strong></div>`).join("")}
        <div class="summary-row summary-total"><span>Total</span><span>${money(state.cart.total_cents)}</span></div>
        <form class="checkout-form" data-form="checkout">
          <div class="field"><label for="payment-outcome">Mock payment result</label>
            <select id="payment-outcome" name="payment_outcome"><option value="success">Success</option><option value="decline">Decline</option><option value="temporary_error">Temporary error</option></select>
            <small>Practice outcomes only. No card or payment details are used.</small>
          </div>
          <button class="button" type="submit">Place order · ${money(state.cart.total_cents)}</button>
        </form>
      </aside></div>` : list}`;
}

function renderOrders() {
  const orders = state.orders;
  content.innerHTML = `
    <div class="page-heading"><div><p class="eyebrow">Your little ledger</p><h1>Orders</h1><p>Each order keeps the product details and prices from the day it was placed.</p></div></div>
    ${orders.length ? `<div class="order-list">${orders.map((order) => `
      <article class="order-card">
        <div class="order-head"><div><strong>Order #${order.id}</strong><br><time>${escapeHtml(displayDate(order.created_at))}</time></div>
          <span class="status-pill" data-status="${escapeHtml(order.status)}">${escapeHtml(order.status)}</span></div>
        <div class="order-lines">${order.items.map((item) => `<div class="order-line"><span>${escapeHtml(item.name)} × ${item.quantity}</span><span>${money(item.line_total_cents)}</span></div>`).join("")}</div>
        <div class="order-foot"><strong class="order-total">${money(order.total_cents)}</strong>
          ${order.status === "placed" ? `<button type="button" class="button button-secondary" data-action="cancel-order" data-order-id="${order.id}">Cancel order</button>` : ""}
        </div>
      </article>`).join("")}</div>` : `
      <div class="empty-state"><strong>No orders yet.</strong><p>Your first market trip will show up here.</p><button class="button button-secondary" type="button" data-view="shop">Browse the market</button></div>`}`;
}

function renderAdminCatalog() {
  return `
    <section class="admin-section" aria-labelledby="catalog-admin-title">
      <div class="admin-section-head"><div><p class="eyebrow">Cove stockroom</p><h2 id="catalog-admin-title">Products & inventory</h2><p>Keep the shelves stocked and product details current.</p></div></div>
      <form class="new-product-form" data-form="create-product">
        <div class="field"><label for="new-product-id">Product ID</label><input id="new-product-id" name="id" required pattern="[a-z0-9]+(-[a-z0-9]+)*" maxlength="80" placeholder="food-new-find"></div>
        <div class="field"><label for="new-product-name">Name</label><input id="new-product-name" name="name" required maxlength="120" placeholder="A new good thing"></div>
        <div class="field"><label for="new-product-category">Category</label><select id="new-product-category" name="category"><option value="food">Food</option><option value="stones">Stones</option><option value="sticks">Sticks</option><option value="toys">Toys</option></select></div>
        <div class="field"><label for="new-product-price">Price (cents)</label><input id="new-product-price" name="price_cents" type="number" min="0" step="1" required value="0"></div>
        <div class="field"><label for="new-product-stock">Stock</label><input id="new-product-stock" name="stock" type="number" min="0" step="1" required value="0"></div>
        <button class="button" type="submit">Add product</button>
      </form>
      <div class="inventory-list">
        ${state.products.map((product) => `
          <article class="inventory-row">
            <div class="inventory-product"><strong>${escapeHtml(product.name)}</strong><small>${escapeHtml(product.id)} · ${escapeHtml(categoryInfo[product.category]?.label || product.category)} · ${money(product.price_cents)}</small></div>
            <form class="stock-adjust-form" data-form="stock-adjust" data-product-id="${escapeHtml(product.id)}">
              <div class="field"><label for="delta-${escapeHtml(product.id)}">Adjust stock</label><input id="delta-${escapeHtml(product.id)}" name="delta" type="number" step="1" value="1" required></div>
              <button class="button button-secondary" type="submit">Apply</button>
            </form>
            <details class="edit-details"><summary>Edit product details</summary>
              <form class="edit-product-form" data-form="edit-product" data-product-id="${escapeHtml(product.id)}">
                <div class="field"><label for="edit-name-${escapeHtml(product.id)}">Name</label><input id="edit-name-${escapeHtml(product.id)}" name="name" value="${escapeHtml(product.name)}" required maxlength="120"></div>
                <div class="field"><label for="edit-category-${escapeHtml(product.id)}">Category</label><select id="edit-category-${escapeHtml(product.id)}" name="category">${Object.entries(categoryInfo).map(([key, value]) => `<option value="${key}" ${key === product.category ? "selected" : ""}>${value.label}</option>`).join("")}</select></div>
                <div class="field"><label for="edit-price-${escapeHtml(product.id)}">Price (cents)</label><input id="edit-price-${escapeHtml(product.id)}" name="price_cents" type="number" min="0" step="1" value="${product.price_cents}" required></div>
                <div class="field"><label for="edit-stock-${escapeHtml(product.id)}">Stock</label><input id="edit-stock-${escapeHtml(product.id)}" name="stock" type="number" min="0" step="1" value="${product.stock}" required></div>
                <button class="button button-quiet" type="submit">Save details</button>
              </form>
            </details>
          </article>`).join("")}
      </div>
    </section>`;
}

function renderAdminOrders() {
  return `
    <section class="admin-section" aria-labelledby="admin-orders-title">
      <div class="admin-section-head"><div><p class="eyebrow">Customer ledger</p><h2 id="admin-orders-title">Orders</h2><p>Purchase details are visible for support. Order status stays with the shopper flow.</p></div><span class="readonly-note">Read only</span></div>
      ${state.adminOrders.length ? state.adminOrders.map((order) => `
        <article class="admin-order-card">
          <div class="admin-order-title"><strong>Order #${order.id}</strong><span>${escapeHtml(order.user_id)}</span><span class="status-pill" data-status="${escapeHtml(order.status)}">${escapeHtml(order.status)}</span></div>
          <strong class="admin-order-total">${money(order.total_cents)}</strong>
          <div class="admin-order-items">${order.items.map((item) => `<div class="order-line"><span>${escapeHtml(item.name)} × ${item.quantity} · ${money(item.price_cents)} each</span><span>${money(item.line_total_cents)}</span></div>`).join("")}</div>
        </article>`).join("") : `<div class="empty-state"><strong>No orders to review.</strong><p>Customer orders will appear here after checkout.</p></div>`}`;
}

function renderAdmin() {
  content.innerHTML = `
    <div class="page-heading"><div><p class="eyebrow">Cove keeper</p><h1>Admin room</h1><p>Keep product details and stock in good shape, then review customer orders.</p></div></div>
    <div class="admin-subnav" role="group" aria-label="Admin pages">
      <button class="filter-button ${state.adminSection === "inventory" ? "is-selected" : ""}" type="button" data-admin-section-btn="inventory" aria-pressed="${state.adminSection === "inventory"}">Products & inventory</button>
      <button class="filter-button ${state.adminSection === "orders" ? "is-selected" : ""}" type="button" data-admin-section-btn="orders" aria-pressed="${state.adminSection === "orders"}">Read-only orders</button>
    </div>
    ${state.adminSection === "inventory" ? renderAdminCatalog() : renderAdminOrders()}`;
}

function render() {
  updateNavigation();
  if (state.view === "shop") renderShop();
  else if (state.view === "cart") renderCart();
  else if (state.view === "orders") renderOrders();
  else renderAdmin();
}

async function refreshProducts() {
  state.products = await api("/products");
}

async function refreshCart() {
  if (!isAdmin()) state.cart = await api("/cart");
}

async function refreshOrders() {
  if (isAdmin()) state.adminOrders = await api("/admin/orders");
  else state.orders = await api("/orders");
}

async function reload() {
  try {
    await refreshProducts();
    if (isAdmin()) {
      await refreshOrders();
    } else {
      await refreshCart();
      if (state.view === "orders") await refreshOrders();
    }
    render();
  } catch (error) {
    render();
    showMessage(error.message || "The market could not be loaded. Check that local seed data is ready.", "error");
  }
}

function goTo(view) {
  if (view === "admin" && !isAdmin()) return;
  if (view !== "admin" && isAdmin()) return;
  state.view = view;
  clearMessage();
  render();
  if (view === "cart") refreshCart().then(render).catch((error) => showMessage(error.message, "error"));
  if (view === "orders") refreshOrders().then(render).catch((error) => showMessage(error.message, "error"));
  if (view === "admin") {
    Promise.all([refreshProducts(), refreshOrders()]).then(render).catch((error) => showMessage(error.message, "error"));
  }
}

async function handleClick(event) {
  const viewButton = event.target.closest("[data-view]");
  if (viewButton) {
    goTo(viewButton.dataset.view);
    return;
  }
  const sectionButton = event.target.closest("[data-admin-section-btn]");
  if (sectionButton) {
    state.adminSection = sectionButton.dataset.adminSectionBtn;
    clearMessage();
    if (state.adminSection === "orders") await refreshOrders();
    render();
    return;
  }
  const categoryButton = event.target.closest("[data-category]");
  if (categoryButton) {
    state.category = categoryButton.dataset.category;
    render();
    return;
  }
  const actionButton = event.target.closest("[data-action]");
  if (!actionButton) return;

  try {
    if (actionButton.dataset.action === "add") {
      state.cart = await api("/cart/items", {
        method: "POST",
        body: { product_id: actionButton.dataset.productId, quantity: 1 },
      });
      showMessage("Added to your basket.", "success");
      render();
    } else if (actionButton.dataset.action === "remove") {
      await api(`/cart/items/${encodeURIComponent(actionButton.dataset.productId)}`, { method: "DELETE" });
      state.cart = await api("/cart");
      showMessage("Removed from your basket.", "success");
      render();
    } else if (actionButton.dataset.action === "cancel-order") {
      await api(`/orders/${actionButton.dataset.orderId}/cancel`, { method: "POST" });
      await Promise.all([refreshOrders(), refreshProducts()]);
      showMessage(`Order #${actionButton.dataset.orderId} was cancelled and its stock restored.`, "success");
      render();
    }
  } catch (error) {
    showMessage(error.message, "error");
    if (!isAdmin()) await Promise.all([refreshProducts(), refreshCart()]).catch(() => {});
    render();
  }
}

async function handleSubmit(event) {
  const form = event.target.closest("form[data-form]");
  if (!form) return;
  event.preventDefault();
  clearMessage();
  const values = new FormData(form);
  const formType = form.dataset.form;
  const number = (key) => Number(values.get(key));

  try {
    if (formType === "cart-quantity") {
      state.cart = await api(`/cart/items/${encodeURIComponent(form.dataset.productId)}`, {
        method: "PUT",
        body: { quantity: number("quantity") },
      });
      showMessage("Basket quantity updated.", "success");
    } else if (formType === "checkout") {
      const outcome = values.get("payment_outcome");
      if (!state.checkoutKey || state.checkoutOutcome !== outcome) {
        state.checkoutKey = crypto.randomUUID();
        state.checkoutOutcome = outcome;
      }
      const order = await api("/checkout", {
        method: "POST",
        headers: { "Idempotency-Key": state.checkoutKey },
        body: { payment_outcome: outcome },
      });
      state.checkoutKey = null;
      state.checkoutOutcome = null;
      state.view = "orders";
      await Promise.all([refreshProducts(), refreshCart(), refreshOrders()]);
      showMessage(`Order #${order.id} is placed. Your cove finds are on their way.`, "success");
      render();
      return;
    } else if (formType === "create-product") {
      await api("/admin/products", {
        method: "POST",
        body: {
          id: values.get("id"),
          name: values.get("name"),
          category: values.get("category"),
          price_cents: number("price_cents"),
          stock: number("stock"),
        },
      });
      form.reset();
      showMessage("Product added to the catalog.", "success");
    } else if (formType === "edit-product") {
      await api(`/admin/products/${encodeURIComponent(form.dataset.productId)}`, {
        method: "PUT",
        body: {
          name: values.get("name"),
          category: values.get("category"),
          price_cents: number("price_cents"),
          stock: number("stock"),
        },
      });
      showMessage("Product details saved.", "success");
    } else if (formType === "stock-adjust") {
      await api(`/admin/products/${encodeURIComponent(form.dataset.productId)}/stock-adjustments`, {
        method: "POST",
        body: { delta: number("delta") },
      });
      showMessage("Stock adjustment saved.", "success");
    }

    await refreshProducts();
    render();
  } catch (error) {
    if (formType === "checkout" && error.status) {
      state.checkoutKey = null;
      state.checkoutOutcome = null;
    }
    showMessage(error.message, "error");
  }
}

nav.addEventListener("click", handleClick);
content.addEventListener("click", handleClick);
content.addEventListener("submit", handleSubmit);
identitySelect.addEventListener("change", async () => {
  state.userId = identitySelect.value;
  state.view = isAdmin() ? "admin" : "shop";
  state.adminSection = "inventory";
  state.checkoutKey = null;
  state.checkoutOutcome = null;
  clearMessage();
  await reload();
});

reload();
