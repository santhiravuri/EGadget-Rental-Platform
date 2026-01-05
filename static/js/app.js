document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('themeToggle');
  const icon = document.getElementById('themeIcon');
  const body = document.body;
  const saved = localStorage.getItem('theme') || 'light';
  if (saved === 'dark') body.classList.add('dark');
  if (icon) icon.className = body.classList.contains('dark') ? 'bi bi-moon-stars-fill' : 'bi bi-moon-stars';
  if (btn) {
    btn.addEventListener('click', () => {
      body.classList.toggle('dark');
      const isDark = body.classList.contains('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      if (icon) icon.className = isDark ? 'bi bi-moon-stars-fill' : 'bi bi-moon-stars';
    });
  }
});

// Home banner auto-rotation
document.addEventListener('DOMContentLoaded', () => {
  const rotator = document.getElementById('heroRotator');
  const titleEl = document.getElementById('heroTitle');
  const subEl = document.getElementById('heroSubtitle');
  if (!rotator) return;
  let images = [];
  let texts = [];
  try {
    images = JSON.parse(rotator.getAttribute('data-banners') || '[]');
    texts = JSON.parse(rotator.getAttribute('data-text') || '[]');
  } catch (e) {
    images = [];
    texts = [];
  }
  if (!Array.isArray(images) || images.length === 0) return;
  let idx = 0;
  function show(i) {
    const url = images[i % images.length];
    rotator.style.backgroundImage = `url("${url}")`;
    // fade in
    rotator.classList.add('is-active');
    // fade out before next switch
    setTimeout(() => {
      rotator.classList.remove('is-active');
    }, 4200);
    const t = texts[i % texts.length];
    if (titleEl && t && t.title) titleEl.textContent = t.title;
    if (subEl && t && t.subtitle) subEl.textContent = t.subtitle;
  }
  show(idx);
  setInterval(() => {
    idx = (idx + 1) % images.length;
    show(idx);
  }, 5000);
});

// Navbar search auto-suggestions
document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('.navbar-search-form input[type="search"]');
  if (!input) return;
  const wrapper = input.parentElement;
  let list = null;
  let debounceTimer = null;
  function ensureList() {
    if (!list) {
      list = document.createElement('div');
      list.className = 'search-suggestions';
      wrapper.appendChild(list);
    }
  }
  async function fetchSuggestions(q) {
    try {
      const res = await fetch(`/api/search/suggest?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      return (data && data.suggestions) || [];
    } catch (e) {
      return [];
    }
  }
  function render(items) {
    ensureList();
    if (!items.length) {
      list.innerHTML = '';
      list.style.display = 'none';
      return;
    }
    list.style.display = 'block';
    list.innerHTML = '';
    items.forEach((s) => {
      const a = document.createElement('a');
      a.href = s.url;
      a.className = 'suggestion-item';
      const label = document.createElement('span');
      label.textContent = s.label;
      const meta = document.createElement('span');
      meta.className = 'meta';
      if (s.type === 'product' && s.meta) {
        const price = s.meta.price ? `₹${s.meta.price}/day` : '';
        const sub = s.meta.subcategory ? ` • ${s.meta.subcategory}` : '';
        meta.textContent = `${s.meta.category || ''}${sub}${price ? ' • ' + price : ''}`;
      } else {
        meta.textContent = s.type === 'subcategory' ? 'Browse' : '';
      }
      a.appendChild(label);
      a.appendChild(meta);
      list.appendChild(a);
    });
  }
  input.addEventListener('input', () => {
    const q = input.value.trim();
    clearTimeout(debounceTimer);
    if (!q) {
      if (list) { list.style.display = 'none'; list.innerHTML = ''; }
      return;
    }
    debounceTimer = setTimeout(async () => {
      const items = await fetchSuggestions(q);
      render(items);
    }, 200);
  });
  // Hide when clicking outside
  document.addEventListener('click', (e) => {
    if (list && !wrapper.contains(e.target)) {
      list.style.display = 'none';
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('notifToggle');
  const dropdown = document.getElementById('notificationDropdown');
  if (!toggle || !dropdown) return;
  let items = JSON.parse(localStorage.getItem('notifications') || '[]');
  if (!Array.isArray(items) || items.length === 0) {
    items = [
      { id: 'n1', label: 'New offer available', time: 'Just now', unread: true },
      { id: 'n2', label: 'Order approved', time: '2h ago', unread: true },
      { id: 'n3', label: 'Payment received', time: '1d ago', unread: false },
    ];
    localStorage.setItem('notifications', JSON.stringify(items));
  }
  function render() {
    dropdown.innerHTML = '';
    items.forEach((n) => {
      const div = document.createElement('div');
      div.className = 'notification-item' + (n.unread ? ' unread' : '');
      const label = document.createElement('span');
      label.className = 'label';
      label.textContent = n.label;
      const time = document.createElement('span');
      time.className = 'time';
      time.textContent = n.time;
      div.appendChild(label);
      div.appendChild(time);
      div.addEventListener('click', () => {
        n.unread = false;
        localStorage.setItem('notifications', JSON.stringify(items));
        render();
        dropdown.classList.remove('is-open');
        const badges = document.querySelectorAll('#notifToggle .badge');
        badges.forEach(b => b.textContent = getUnreadCount());
      });
      dropdown.appendChild(div);
    });
  }
  function getUnreadCount() {
    return items.filter(i => i.unread).length || '';
  }
  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    if (dropdown.classList.contains('is-open')) {
      dropdown.classList.remove('is-open');
    } else {
      render();
      dropdown.classList.add('is-open');
    }
  });
  document.addEventListener('click', (e) => {
    if (!dropdown.contains(e.target) && !toggle.contains(e.target)) {
      dropdown.classList.remove('is-open');
    }
  });
});

// Toast Notification Function
function showToast(message, type = 'success') {
  const toastContainer = document.getElementById('toastContainer');
  if (!toastContainer) return;
  
  const toast = document.createElement('div');
  toast.className = `toast custom-toast show`;
  toast.setAttribute('role', 'alert');
  toast.innerHTML = `
    <div class="toast-header">
      <strong class="me-auto">${type === 'success' ? 'Success' : 'Info'}</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    </div>
    <div class="toast-body">${message}</div>
  `;
  
  toastContainer.appendChild(toast);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Enhanced Add to Cart with Animation
document.addEventListener('submit', async (e) => {
  const form = e.target;
  if (form.matches('#add-to-cart')) {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerHTML : '';
    
    // Add animation class
    if (submitBtn) {
      submitBtn.classList.add('adding', 'btn-cart-add');
      submitBtn.disabled = true;
    }
    
    const formData = new FormData(form);
    try {
      const res = await fetch(form.action, { method: 'POST', body: formData });
      const data = await res.json();
      
      if (data.ok) {
        // Update cart badge with animation
        const badge = document.querySelector('.navbar .badge');
        if (badge) {
          badge.textContent = data.cart_count;
          badge.classList.add('cart-icon-animation');
          setTimeout(() => badge.classList.remove('cart-icon-animation'), 600);
        }
        
        // Show toast notification
        showToast('Item added to cart!', 'success');
        
        // Reset button
        if (submitBtn) {
          setTimeout(() => {
            submitBtn.classList.remove('adding');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
          }, 500);
        }
      } else {
        showToast(data.message || 'Failed to add item to cart', 'error');
        if (submitBtn) {
          submitBtn.classList.remove('adding');
          submitBtn.disabled = false;
        }
      }
    } catch (error) {
      showToast('An error occurred. Please try again.', 'error');
      if (submitBtn) {
        submitBtn.classList.remove('adding');
        submitBtn.disabled = false;
      }
    }
  }
});

// Wishlist Toggle with Animation
document.addEventListener('submit', async (e) => {
  const form = e.target;
  if (form.action && form.action.includes('/api/wishlist/toggle')) {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerHTML : '';
    
    // Add animation class
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i>';
    }
    
    const formData = new FormData(form);
    try {
      const res = await fetch(form.action, { method: 'POST', body: formData });
      const data = await res.json();
      
      if (data.ok) {
        // Update wishlist badge
        const wishlistBadge = document.querySelector('a[href*="wishlist"] .badge');
        if (wishlistBadge) {
          const newCount = data.wishlist_count || 0;
          wishlistBadge.textContent = newCount;
          if (newCount > 0) {
            wishlistBadge.style.display = 'inline-block';
          } else {
            wishlistBadge.style.display = 'none';
          }
        }
        
        // If on wishlist page, remove the card
        if (window.location.pathname === '/wishlist') {
          const card = form.closest('.col-6, .col-md-4, .col-lg-3');
          if (card) {
            card.style.transition = 'opacity 0.3s';
            card.style.opacity = '0';
            setTimeout(() => card.remove(), 300);
            showToast('Item removed from wishlist!', 'success');
          }
        } else {
          // Toggle button text
          if (submitBtn) {
            const isInWishlist = data.in_wishlist;
            submitBtn.innerHTML = isInWishlist ? '<i class="bi bi-heart-fill me-1"></i> Saved' : '<i class="bi bi-heart me-1"></i> Save to Wishlist';
            submitBtn.classList.toggle('btn-danger', isInWishlist);
            submitBtn.classList.toggle('btn-outline-danger', !isInWishlist);
          }
          showToast(data.in_wishlist ? 'Added to wishlist!' : 'Removed from wishlist!', 'success');
        }
        
        // Reset button
        if (submitBtn && window.location.pathname !== '/wishlist') {
          setTimeout(() => {
            submitBtn.disabled = false;
          }, 500);
        }
      } else {
        showToast(data.message || 'Failed to update wishlist', 'error');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;
        }
      }
    } catch (error) {
      showToast('An error occurred. Please try again.', 'error');
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    }
  }
});

// Mega category menu (click + hover)
document.addEventListener('DOMContentLoaded', () => {
  const megaMenu = document.getElementById('megaMenu');
  const megaTitle = document.getElementById('megaTitle');
  const megaGrid = document.getElementById('megaGrid');
  const categoryNav = document.querySelector('.category-nav');
  const categoryLinks = document.querySelectorAll('.category-link[data-category]');

  if (!megaMenu || !megaTitle || !megaGrid || !categoryNav || !categoryLinks.length) {
    return;
  }

  const MEGA_DATA = {
    'Mobiles': [
      'Smartphones',
      'Feature Phones',
      'Tablets',
      'Mobile Accessories',
      'Refurbished Mobiles',
    ],
    'Laptops': [
      'Laptops',
      'Gaming Laptops',
      'Desktops',
      'Monitors',
      'Keyboards & Mouse',
    ],
    'Cameras': [
      'DSLR',
      'Mirrorless',
      'Action Cameras',
      'Webcams',
      'Drones',
    ],
    'Headphones': [
      'Wired Headphones',
      'Wireless Headphones',
      'Earbuds',
      'Bluetooth Speakers',
      'Sound Bars',
    ],
    'Smart Watches': [
      'Smart Watches',
      'Fitness Bands',
      'Health Trackers',
    ],
    'Gaming Consoles': [
      'PlayStation',
      'Xbox',
      'Handheld Console',
      'Controllers',
      'VR Headsets',
    ],
    'Accessories': [
      'Chargers',
      'Power Banks',
      'Cables',
      'Storage Devices',
      'Adaptors',
    ],
  };
  // Expose for other modules
  window.MEGA_DATA = MEGA_DATA;

  let currentCategory = null;
  let hoverTimeout = null;

  function populateMega(category) {
    megaTitle.textContent = category;
    megaGrid.innerHTML = '';

    const items = MEGA_DATA[category] || [];
    items.forEach((label) => {
      const link = document.createElement('a');
      // Navigate to catalog filtered by category and subcategory
      link.href = `/catalog?category=${encodeURIComponent(category)}&sub=${encodeURIComponent(label)}`;
      link.className = 'mega-item';
      link.textContent = label;
      link.dataset.subcategory = label;
      megaGrid.appendChild(link);
    });
  }

  function positionMegaMenu(activeLink) {
    if (!activeLink || !megaMenu) return;
    
    const categoryNav = activeLink.closest('.category-nav');
    if (!categoryNav) return;
    
    const navRect = categoryNav.getBoundingClientRect();
    const linkRect = activeLink.getBoundingClientRect();
    const menuRect = megaMenu.getBoundingClientRect();
    
    // Calculate left position relative to the category nav
    let leftPos = linkRect.left - navRect.left;
    
    // Center align the menu under the link (menu center aligns with link center)
    const linkCenter = linkRect.left + (linkRect.width / 2);
    const menuCenter = menuRect.width / 2;
    leftPos = linkCenter - navRect.left - menuCenter;
    
    // Ensure menu doesn't go off the left edge
    leftPos = Math.max(0, leftPos);
    
    // Ensure menu doesn't go off the right edge
    const maxLeft = navRect.width - menuRect.width;
    if (leftPos > maxLeft) {
      leftPos = Math.max(0, maxLeft);
    }
    
    megaMenu.style.left = `${leftPos}px`;
  }

  function openMega(category, activeLink) {
    if (!category || !MEGA_DATA[category]) {
      closeMega();
      return;
    }
    if (currentCategory === category && megaMenu.classList.contains('is-open')) {
      return;
    }
    currentCategory = category;
    populateMega(category);
    
    // Position menu under the active category item
    if (activeLink) {
      // Use requestAnimationFrame to ensure menu is rendered before positioning
      requestAnimationFrame(() => {
        positionMegaMenu(activeLink);
      });
    }
    
    megaMenu.classList.add('is-open');
    megaMenu.setAttribute('aria-hidden', 'false');
  }

  function closeMega() {
    currentCategory = null;
    megaMenu.classList.remove('is-open');
    megaMenu.setAttribute('aria-hidden', 'true');
  }

  categoryLinks.forEach((link) => {
    const category = link.dataset.category;
    if (!category) return;

    // Click: navigate to catalog for the category
    link.addEventListener('click', (e) => {
      e.preventDefault();
      window.location.href = `/catalog?category=${encodeURIComponent(category)}`;
    });

    // Hover: temporarily show dropdown
    link.addEventListener('mouseenter', () => {
      if (hoverTimeout) {
        clearTimeout(hoverTimeout);
        hoverTimeout = null;
      }
      openMega(category, link);
    });
  });

  // Keep menu open while hovering over the mega menu itself
  megaMenu.addEventListener('mouseenter', () => {
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
      hoverTimeout = null;
    }
  });

  megaMenu.addEventListener('mouseleave', () => {
    hoverTimeout = setTimeout(() => {
      closeMega();
    }, 150);
  });

  // Close when leaving the whole category nav area
  if (categoryNav) {
    categoryNav.addEventListener('mouseleave', () => {
      hoverTimeout = setTimeout(() => {
        closeMega();
      }, 150);
    });
  }

  // Clicking outside closes the mega menu
  document.addEventListener('click', (e) => {
    if (!megaMenu.classList.contains('is-open')) return;
    if (categoryNav.contains(e.target) || megaMenu.contains(e.target)) {
      return;
    }
    closeMega();
  });

  // Reposition menu on window resize if it's open
  window.addEventListener('resize', () => {
    if (megaMenu.classList.contains('is-open') && currentCategory) {
      const activeLink = Array.from(categoryLinks).find(
        link => link.dataset.category === currentCategory
      );
      if (activeLink) {
        positionMegaMenu(activeLink);
      }
    }
  });
});

// Category Image Showcase
document.addEventListener('DOMContentLoaded', () => {
  const showcaseContainer = document.getElementById('categoryShowcaseGrid');
  if (!showcaseContainer) return;

  // Image mapping for each category (using placeholder/stock images)
  const CATEGORY_IMAGES = {
    'Mobiles': [
      'https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=400&h=400&fit=crop',
      'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcS_c3Nvbsmn_c2N60Hz-_zc3ZDdq9KO6ph_egSj_yWOtEyVQb0rMultaAUy1k2n7lnBdTPZi7EdykiuYEoA9gYDuhVXqyGacFn5vgF03aKl08f1m45w8hXTXg',
      'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQUAsfZrd-lhpVT2migo03oUSbsQsOlLlJPC6ErkrJwg3PYKhviQvKPnU1ayUQqCp6kPdqQNJkCMZtQxkjREyJuU0Fm4_V6Oro1RbuLuPGO68D1FqpP07V_fQ',
      'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=400&fit=crop',
    ],
    'Laptops': [
      'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&h=400&fit=crop',
    ],
    'Cameras': [
      'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop',
    ],
    'Headphones': [
      'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400&h=400&fit=crop',
    ],
    'Smart Watches': [
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
    ],
    'Gaming Consoles': [
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
    ],
    'Accessories': [
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
    ],
    'Tablets': [
      'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
    ],
    'default': [
      'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
      'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400&h=400&fit=crop',
    ],
  };

  // Main categories list
  const MAIN_CATEGORIES = [
    'Mobiles',
    'Laptops',
    'Cameras',
    'Headphones',
    'Smart Watches',
    'Gaming Consoles',
    'Accessories'
  ];

  function updateShowcase() {
    if (!showcaseContainer) return;
    
    showcaseContainer.innerHTML = '';
    
    // Create one card per main category with its own image and label
    MAIN_CATEGORIES.forEach((categoryName) => {
      // Get the first image for this category (or use default if category doesn't exist)
      const categoryImages = CATEGORY_IMAGES[categoryName] || CATEGORY_IMAGES['default'];
      const imgUrl = categoryImages[0] || CATEGORY_IMAGES['default'][0];
      
      // Create card container
      const card = document.createElement('div');
      card.className = 'category-card';
      
      // Create image item
      const item = document.createElement('div');
      item.className = 'category-showcase-item';
      const img = document.createElement('img');
      img.src = imgUrl;
      img.alt = `${categoryName} category`;
      img.loading = 'lazy';
      item.appendChild(img);
      
      // Create label with unique category name
      const label = document.createElement('p');
      label.className = 'category-label';
      label.textContent = categoryName;
      
      // Append image and label to card
      card.appendChild(item);
      card.appendChild(label);
      showcaseContainer.appendChild(card);
      
      card.addEventListener('click', () => {
        window.location.href = `/catalog?category=${encodeURIComponent(categoryName)}`;
      });
    });
  }

  // Get category from URL parameter on page load
  function getCategoryFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('category') || null;
  }

  // Initialize showcase on page load - show all main categories
  updateShowcase();
  
  const panel = document.getElementById('subcategoryPanel');
}
);

// Chatbot Functionality
document.addEventListener('DOMContentLoaded', () => {
  const chatbotToggle = document.getElementById('chatbotToggle');
  const chatbotContainer = document.getElementById('chatbotContainer');
  const chatbotClose = document.getElementById('chatbotClose');
  const chatbotInput = document.getElementById('chatbotInput');
  const chatbotSend = document.getElementById('chatbotSend');
  const chatbotMessages = document.getElementById('chatbotMessages');
  
  if (!chatbotToggle || !chatbotContainer) return;
  
  // FAQ responses
  const faqResponses = {
    'rental': 'To rent a gadget, browse our catalog, select the item you want, choose rental duration, and add to cart. Complete checkout and we\'ll process your request.',
    'payment': 'We accept all major payment methods. Payment is processed securely at checkout. For payment issues, please contact our support team.',
    'return': 'Items should be returned by the end date specified. Late returns incur a penalty of ₹50 per day. Please return items in the same condition you received them.',
    'damage': 'You are responsible for any damage beyond normal wear and tear. A damage fee will be charged based on the extent of damage.',
    'duration': 'You can rent items for a minimum of 1 day. Maximum rental duration depends on product availability.',
    'penalty': 'Late returns are charged ₹50 per day for each day past the due date. Please return items on time to avoid penalties.',
    'default': 'I\'m here to help! I can answer questions about rentals, payments, returns, and policies. For specific issues, please contact our admin support.'
  };
  
  function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.innerHTML = `<p>${text}</p>`;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }
  
  function processMessage(message) {
    const lowerMessage = message.toLowerCase();
    let response = faqResponses.default;
    
    if (lowerMessage.includes('rent') || lowerMessage.includes('how to') || lowerMessage.includes('process')) {
      response = faqResponses.rental;
    } else if (lowerMessage.includes('pay') || lowerMessage.includes('payment') || lowerMessage.includes('money')) {
      response = faqResponses.payment;
    } else if (lowerMessage.includes('return') || lowerMessage.includes('give back')) {
      response = faqResponses.return;
    } else if (lowerMessage.includes('damage') || lowerMessage.includes('broken')) {
      response = faqResponses.damage;
    } else if (lowerMessage.includes('duration') || lowerMessage.includes('how long') || lowerMessage.includes('days')) {
      response = faqResponses.duration;
    } else if (lowerMessage.includes('penalty') || lowerMessage.includes('late') || lowerMessage.includes('fee')) {
      response = faqResponses.penalty;
    } else if (lowerMessage.includes('contact') || lowerMessage.includes('admin') || lowerMessage.includes('support')) {
      response = 'For direct support, please visit our Contact Us page or email support@egadgetrent.com';
    }
    
    setTimeout(() => addMessage(response), 300);
  }
  
  function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    chatbotInput.value = '';
    
    // Simulate typing delay
    setTimeout(() => processMessage(message), 500);
  }
  
  chatbotToggle.addEventListener('click', () => {
    chatbotContainer.classList.add('active');
    chatbotInput.focus();
  });
  
  if (chatbotClose) {
    chatbotClose.addEventListener('click', () => {
      chatbotContainer.classList.remove('active');
    });
  }
  
  if (chatbotSend) {
    chatbotSend.addEventListener('click', sendMessage);
  }
  
  if (chatbotInput) {
    chatbotInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  }
});
