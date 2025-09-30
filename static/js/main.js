document.addEventListener('DOMContentLoaded', function() {
    // --- Logic for the Main Page (home.html) ---
    const homePageContent = document.querySelector('.main-content-grid');
    if (homePageContent) {
        const keywordsList = document.querySelector('.keywords-list');
        const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
        const sortButtons = document.querySelectorAll('.sort-options .sort-button');

        function checkboxChangeHandler(event) {
            const keyword = this.dataset.keyword;
            if (this.checked) {
                if (!document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`)) {
                    const newTag = document.createElement('span');
                    newTag.className = 'keyword-tag';
                    newTag.setAttribute('data-keyword', keyword);
                    newTag.innerHTML = `${keyword} <i class="fa-solid fa-xmark remove-keyword-icon"></i>`;
                    keywordsList.appendChild(newTag);
                }
            } else {
                const tagToRemove = document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`);
                if (tagToRemove) {
                    tagToRemove.remove();
                }
            }
        }

        function updateHomePageContent(){
            const urlParams = new URLSearchParams(window.location.search);
            const cats = urlParams.get('categories');
            const q = urlParams.get('q');
            const sort = urlParams.get('sort');

            // Logic for categories
            checkboxes.forEach(checkbox => {
                if (cats && cats.includes(checkbox.dataset.keyword)){
                    checkbox.checked = true;
                    checkboxChangeHandler.call(checkbox);
                }
                else {
                    checkbox.checked = false;
                }
            });

            // So that the active sort button lights up
            if (sort) {
                const activeSortButton = document.querySelector(`.sort-options .sort-button[data-sort="${sort}"]`);
                if(activeSortButton){
                    activeSortButton.classList.add('active-sort');
                }
            }
        }

        updateHomePageContent();

        // 1. Sort Options Logic
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active-sort'));
                this.classList.add('active-sort');
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('sort', this.dataset.sort);
                urlParams.set('page', 1);
                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        });

        // 2. Pagination Logic
        const paginationList = document.querySelector('.pagination-list');
        if (paginationList) {
            const paginationLinks = paginationList.querySelectorAll('.pagination__link');
            paginationLinks.forEach(link => {
                link.addEventListener('click', function(event) {
                    event.preventDefault();
                    paginationLinks.forEach(lnk => lnk.classList.remove('active'));
                    this.classList.add('active');
                });
            });
        }

        // 3. Filter Logic (Keywords and Checkboxes)
        const filterButton = document.querySelector('#filter-button');

        if (filterButton){
            filterButton.addEventListener('click', function(){
                const cats = [];
                checkboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        cats.push(checkbox.dataset.keyword);
                    }
                });

                const urlParams = new URLSearchParams(window.location.search);
                if(urlParams.has('page')) { urlParams.delete('page'); }
                urlParams.set('categories', cats);

                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        }

        if (keywordsList && checkboxes.length > 0) {

            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', checkboxChangeHandler);
            });

            keywordsList.addEventListener('click', function(event) {
                const keywordIcon = event.target.closest('.remove-keyword-icon');
                if (keywordIcon) {
                    const keywordTag = keywordIcon.closest('.keyword-tag');
                    const keywordText = keywordTag.dataset.keyword;
                    const checkbox = document.querySelector(`.checkbox-container input[data-keyword="${keywordText}"]`);
                    if (checkbox) {
                        checkbox.checked = false;
                    }
                    keywordTag.remove();
                }
            });
        }

        // 4. Search logic
        const searchInput = document.querySelector('.search-input');
        if (searchInput){
            const searchButton = document.querySelector('.search-button');
            searchButton.addEventListener('click', function(){
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('q', searchInput.value);
                urlParams.set('page', 1);
                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        }
    }

    // --- Logic for Product Detail Pages (product-*.html) ---
    const productPageContent = document.querySelector('.page-product');
    if (productPageContent) {
        // Accordion
        const accordionTitle = document.querySelector('.accordion-title');
        if (accordionTitle) {
            accordionTitle.addEventListener('click', function() {
                this.closest('.accordion-item').classList.toggle('active');
            });
        }
        // "Add to Cart" Button and Counter
        const cartControls = document.querySelector('.cart-controls');
        if (cartControls) {
            const addToCartBtn = cartControls.querySelector('#add-to-cart-btn');
            const quantityCounter = cartControls.querySelector('#quantity-counter');
            const decreaseBtn = quantityCounter.querySelector('[data-action="decrease"]');
            const increaseBtn = quantityCounter.querySelector('[data-action="increase"]');
            const quantityValueSpan = quantityCounter.querySelector('.quantity-value');
            let quantity = Number(quantityValueSpan.dataset.qty) || 0;;
            function updateView() {
                if (quantity === 0) {
                    addToCartBtn.classList.remove('is-hidden');
                    quantityCounter.classList.add('is-hidden');
                } else {
                    addToCartBtn.classList.add('is-hidden');
                    quantityCounter.classList.remove('is-hidden');
                    quantityValueSpan.textContent = `${quantity} in cart`;
                }
            }
            addToCartBtn.addEventListener('click', function() { quantity = 1; updateView(); });
            decreaseBtn.addEventListener('click', function() { if (quantity > 0) { quantity--; updateView(); } });
            increaseBtn.addEventListener('click', function() { quantity++; updateView(); });
            updateView();
        }
    }

    // --- Logic for Cart Page (cart.html) ---
    const cartPageContent = document.querySelector('.cart-page-wrapper');
    if (cartPageContent) {
        const cartItemsList = document.getElementById('cart-items-list');
        const cartTotalPriceElem = document.getElementById('cart-total-price');
        function updateCartTotal() {
            let total = 0;
            document.querySelectorAll('.cart-item').forEach(item => {
                const priceText = item.querySelector('[data-item-total-price]').textContent;
                if (priceText) {
                    total += parseFloat(priceText.replace('$', ''));
                }
            });
            if (cartTotalPriceElem) cartTotalPriceElem.textContent = `$${total.toFixed(2)}`;
        }
        if (cartItemsList) {
            cartItemsList.addEventListener('click', function(event) {
                const cartItem = event.target.closest('.cart-item');
                if (!cartItem) return;
                const quantityElem = cartItem.querySelector('.quantity-value-cart');
                const itemTotalElem = cartItem.querySelector('[data-item-total-price]');
                const basePrice = parseFloat(cartItem.dataset.price);
                let quantity = parseInt(quantityElem.textContent);
                if (event.target.closest('[data-action="increase"]')) {
                    quantity++;
                } else if (event.target.closest('[data-action="decrease"]')) {
                    quantity = quantity > 1 ? quantity - 1 : 0;
                }
                if (quantity != 0) {
                    quantityElem.textContent = quantity;
                    itemTotalElem.textContent = `$${(basePrice * quantity).toFixed(2)}`;
                }
                updateCartTotal();
            });
        }
        updateCartTotal();
    }

    // --- Logic for Account and Admin Pages ---
    const accountAdminWrapper = document.querySelector('.account-page-wrapper, .admin-page-wrapper');
    if (accountAdminWrapper) {
        // Account Page Tabs
        const accountTabs = document.querySelectorAll('.account-tab');
        const tabPanes = document.querySelectorAll('.tab-pane');
        if (accountTabs.length > 0 && tabPanes.length > 0) {
            accountTabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    accountTabs.forEach(item => item.classList.remove('active'));
                    tabPanes.forEach(pane => pane.classList.remove('active'));
                    const targetPane = document.querySelector(this.dataset.tabTarget);
                    this.classList.add('active');
                    if (targetPane) targetPane.classList.add('active');
                });
            });
        }

        // Admin Panel - Category Tags
        const categoryTagsContainer = document.querySelector('.category-tags');
        if (categoryTagsContainer) {
            categoryTagsContainer.addEventListener('click', function(e) {
                const clickedTag = e.target.closest('.category-tag');
                if (clickedTag) {
                    categoryTagsContainer.querySelectorAll('.category-tag').forEach(t => t.classList.remove('active'));
                    clickedTag.classList.add('active');
                }
            });
        }

        // Image Upload Simulation
        const uploadButton = document.getElementById('upload-image-btn');
        const fileInput = document.getElementById('image-upload-input');

        if (uploadButton && fileInput) {
            uploadButton.addEventListener('click', function() {
                fileInput.click();
            });

            fileInput.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    const placeholder = document.querySelector('.image-upload-placeholder');

                    reader.onload = function(e) {
                        placeholder.innerHTML = '';
                        placeholder.style.backgroundImage = `url('${e.target.result}')`;
                        placeholder.style.backgroundSize = 'cover';
                        placeholder.style.backgroundPosition = 'center';
                    }
                    reader.readAsDataURL(file);
                }
            });
        }
    }

    // --- Logic for Modal Review Window in Orders Info
    let selectedRating = 0;
    let focusedElementBeforeModal = null;

    const modal = document.getElementById('review-modal');
    const form = document.getElementById('review-form');
    const title = document.getElementById('review-modal-title');
    const productName = document.getElementById('review-product-name');
    const productImg = document.getElementById('review-product-img');
    const stars = document.querySelectorAll('#review-stars .star');
    const headCommentEl = document.getElementById('review-head-comment');
    const commentEl = document.getElementById('review-comment');
    const orderIdInput = document.getElementById('review-order-id');
    const ratingInput = document.getElementById('review-rating');

    function syncHiddenRating() {
      ratingInput.value = selectedRating || '';
    }

    function openModal(btn) {
      focusedElementBeforeModal = document.activeElement;
      form.action = btn.dataset.url;
      orderIdInput.value = btn.dataset.orderId || '';
      productName.textContent = btn.dataset.productName || '';
      productImg.src = btn.dataset.productImage || btn.dataset.productImg || '';
      productImg.alt = btn.dataset.productName ? `Image of ${btn.dataset.productName}` : 'Product image';

      // prefill
      const countStars = parseInt(btn.dataset.existingRating || '5', 10);
      selectedRating = Number.isFinite(countStars) && countStars > 0 ? countStars : 5;
      stars.forEach((s, i) => {
        s.style.color = i < selectedRating ? '#ffc107' : '#ddd';
      });
      syncHiddenRating();

      const headComment = btn.dataset.existingHeadComment || '';
      const comment = btn.dataset.existingComment || '';
      headCommentEl.value = headComment;
      commentEl.value = comment;

      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      form.reset();
      selectedRating = 0;
      syncHiddenRating();

      if (focusedElementBeforeModal) { focusedElementBeforeModal.focus(); }
    }

    function rateStars(){
        stars.forEach((star, index) => {
            star.addEventListener('mouseover', () => {
                stars.forEach((s, i) => {
                    s.style.color = i <= index ? '#ffc107' : '#ddd';
                });
            });

            star.addEventListener('mouseout', () => {
                stars.forEach((s, i) => {
                    s.style.color = i < selectedRating ? '#ffc107' : '#ddd';
                });
            });

            star.addEventListener('click', () => {
                selectedRating = index + 1;
                stars.forEach((s, i) => {
                    s.style.color = i < selectedRating ? '#ffc107' : '#ddd';
                });
                syncHiddenRating();
            });
        });
    }

    // open
    document.addEventListener('click', function(e) {
      const btn = e.target.closest('.js-open-review');
      if (btn) {
        e.preventDefault();
        openModal(btn);
      }
    });

    // close
    document.addEventListener('click', function(e) {
      if (e.target.closest('.js-close-review')) {
        e.preventDefault();
        closeModal();
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeModal();
    });

    rateStars();
});