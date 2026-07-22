// ============================================
// MarkosDev — interações (vanilla JS)
// ============================================

document.addEventListener("DOMContentLoaded", () => {
  /* ---------- Tema (dark/light) ---------- */
  const root = document.documentElement
  const themeToggle = document.getElementById("theme-toggle")
  const themeIcon = document.getElementById("theme-icon")

  function applyTheme(dark) {
    root.classList.toggle("dark", dark)
    themeIcon.setAttribute("data-lucide", dark ? "sun" : "moon")
    themeToggle.setAttribute("aria-label", dark ? "Ativar modo claro" : "Ativar modo escuro")
    if (typeof lucide !== "undefined") lucide.createIcons()
  }

  const stored = localStorage.getItem("markosdev-theme")
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
  let isDark = stored ? stored === "dark" : prefersDark
  applyTheme(isDark)

  themeToggle.addEventListener("click", () => {
    isDark = !isDark
    applyTheme(isDark)
    localStorage.setItem("markosdev-theme", isDark ? "dark" : "light")
  })

  /* ---------- Menu mobile ---------- */
  const sidebar = document.getElementById("sidebar")
  const overlay = document.getElementById("sidebar-overlay")
  const openMenu = document.getElementById("open-menu")
  const closeMenu = document.getElementById("close-menu")

  function setMenu(open) {
    sidebar.classList.toggle("open", open)
    overlay.classList.toggle("show", open)
  }

  openMenu.addEventListener("click", () => setMenu(true))
  closeMenu.addEventListener("click", () => setMenu(false))
  overlay.addEventListener("click", () => setMenu(false))
  document.querySelectorAll("[data-close-menu]").forEach((el) => {
    el.addEventListener("click", () => setMenu(false))
  })

  /* ---------- Dropdown "Área do Cliente" ---------- */
  const clientToggle = document.getElementById("client-toggle")
  const clientDropdown = document.getElementById("client-dropdown")
  const clientChevron = document.getElementById("client-chevron")
  const clientLoginBtnDropdown = document.getElementById("client-login-btn")
  const clientRegisterBtn = document.getElementById("client-register-btn")
  const clientRegisterModal = document.getElementById("client-register-modal")
  const clientRegisterClose = document.getElementById("client-register-close")
  const clientRegisterCancel = document.getElementById("client-register-cancel")
  const clientRegisterForm = document.getElementById("client-register-form")
  const clientRegisterMessage = document.getElementById("client-register-message")

  function setClientMenu(open) {
    clientDropdown.hidden = !open
    clientToggle.setAttribute("aria-expanded", String(open))
    clientChevron.classList.toggle("rotate", open)
  }

  clientToggle.addEventListener("click", (e) => {
    e.stopPropagation()
    setClientMenu(clientDropdown.hidden)
  })

  function openClientRegisterModal() {
    setClientMenu(false)
    clientRegisterModal.hidden = false
    clientRegisterMessage.hidden = true
    clientRegisterMessage.textContent = ""
    clientRegisterForm.reset()
    document.getElementById("client-register-name")?.focus()
  }

  function closeClientRegisterModal() {
    clientRegisterModal.hidden = true
  }

  clientLoginBtnDropdown?.addEventListener("click", (e) => {
    e.stopPropagation()
    setClientMenu(false)
    setClientAreaLoggedIn(false)
    if (window.location.hash !== "#cliente") {
      window.location.hash = "#cliente"
    } else {
      handleNavigation()
    }
    document.getElementById("cliente")?.scrollIntoView({ behavior: "smooth", block: "start" })
    clientEmailInput?.focus()
  })

  clientRegisterBtn?.addEventListener("click", (e) => {
    e.stopPropagation()
    openClientRegisterModal()
  })
  clientRegisterClose?.addEventListener("click", closeClientRegisterModal)
  clientRegisterCancel?.addEventListener("click", closeClientRegisterModal)
  clientRegisterModal?.addEventListener("click", (e) => {
    if (e.target === clientRegisterModal) closeClientRegisterModal()
  })

  clientRegisterForm?.addEventListener("submit", async (e) => {
    e.preventDefault()
    const formData = new FormData(clientRegisterForm)
    const payload = Object.fromEntries(formData.entries())

    try {
      const response = await fetch("/api/clients", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "servidor fora do ar" }))
        throw new Error(parseServerError(errorData))
      }

      clientRegisterForm.reset()
      closeClientRegisterModal()
      requestAnimationFrame(() => {
        window.setTimeout(() => {
          alert("Cadastro efetuado com sucesso!")
        }, 50)
      })
    } catch (error) {
      alert(error.message || "servidor fora do ar")
    }
  })

  document.addEventListener("click", (e) => {
    if (!clientDropdown.contains(e.target) && !clientToggle.contains(e.target)) {
      setClientMenu(false)
    }
  })

  /* ---------- Área do Cliente ---------- */
  const clientLoginSection = document.getElementById("client-area-login")
  const clientDashboardSection = document.getElementById("client-area-dashboard")
  const clientEmailInput = document.getElementById("client-email")
  const clientPasswordInput = document.getElementById("client-password")
  const clientLoginSubmitBtn = document.getElementById("client-login-submit-btn")
  const clientLoginError = document.getElementById("client-login-error")
  const clientMessagesList = document.getElementById("client-messages-list")
  const clientWelcomeText = document.getElementById("client-welcome-text")
  const clientNewBtn = document.getElementById("client-new-btn")
  const clientLogoutBtn = document.getElementById("client-logout-btn")
  const clientMessageModal = document.getElementById("client-message-modal")
  const clientMessageModalClose = document.getElementById("client-message-modal-close")
  const clientMessageModalCancel = document.getElementById("client-message-modal-cancel")
  const clientMessageForm = document.getElementById("client-message-form")
  const clientMessageModalTitle = document.getElementById("client-message-modal-title")
  const clientMessageId = document.getElementById("client-message-id")
  const clientMessageTitle = document.getElementById("client-message-title")
  const clientMessageContent = document.getElementById("client-message-content")
  const clientMessageAttachment = document.getElementById("client-message-attachment")
  const clientMessageStatus = document.getElementById("client-message-status")
  const clientMessageSave = document.getElementById("client-message-save")

  let clientAuth = null
  let clientMessages = []

  function setClientAreaLoggedIn(loggedIn) {
    clientLoginSection.hidden = loggedIn
    clientDashboardSection.hidden = !loggedIn
    if (loggedIn && clientAuth) {
      clientWelcomeText.textContent = `Olá, ${clientAuth.name}! Aqui estão suas mensagens.`
    }
    if (!loggedIn) {
      clientLoginError.hidden = true
      clientLoginError.textContent = ""
      clientEmailInput.value = ""
      clientPasswordInput.value = ""
      clientMessagesList.innerHTML = ""
      clientWelcomeText.textContent = ""
      clientAuth = null
      clientMessages = []
      localStorage.removeItem("markosdev_client_auth")
    }
  }

  function formatClientMessageDateTime(iso) {
    const date = new Date(iso)
    if (Number.isNaN(date.getTime())) return iso
    return new Intl.DateTimeFormat("pt-BR", {
      dateStyle: "short",
      timeStyle: "short",
    }).format(date)
  }

  function renderClientMessages(items) {
    if (!items.length) {
      clientMessagesList.innerHTML = '<p class="admin-empty">Nenhuma mensagem cadastrada.</p>'
      return
    }

    clientMessagesList.innerHTML = ""
    const list = document.createElement("div")
    list.className = "client-message-list"

    items.forEach((item) => {
      const card = document.createElement("article")
      card.className = "client-message-card"
      card.innerHTML = `
        <div class="client-message-main">
          <h4 class="client-message-title">${item.title}</h4>
          <p class="client-message-meta">${formatClientMessageDateTime(item.created_at)} · ${item.status || "pendente"}</p>
        </div>
        <div class="client-message-actions">
          <button class="icon-btn edit-btn" data-id="${item.id}" aria-label="Editar"><i data-lucide="pencil"></i></button>
          <button class="icon-btn delete-btn" data-id="${item.id}" aria-label="Excluir"><i data-lucide="trash-2"></i></button>
        </div>
      `
      list.appendChild(card)
    })

    clientMessagesList.appendChild(list)
    if (typeof lucide !== "undefined") lucide.createIcons()

    clientMessagesList.querySelectorAll(".edit-btn").forEach((btn) => {
      btn.addEventListener("click", () => openClientMessageModal(Number(btn.dataset.id)))
    })
    clientMessagesList.querySelectorAll(".delete-btn").forEach((btn) => {
      btn.addEventListener("click", () => deleteClientMessage(Number(btn.dataset.id)))
    })
  }

  async function loadClientMessages() {
    if (!clientAuth) return
    try {
      const response = await fetch(`/api/clients/${clientAuth.id}/messages`)
      if (!response.ok) throw new Error("Erro ao carregar mensagens")
      clientMessages = await response.json()
      renderClientMessages(clientMessages)
    } catch (error) {
      clientMessagesList.innerHTML = '<p class="admin-empty">Não foi possível carregar suas mensagens.</p>'
    }
  }

  function closeClientMessageModal() {
    clientMessageModal.hidden = true
  }

  function openClientMessageModal(messageId = null) {
    clientMessageModalTitle.textContent = messageId ? "Editar Mensagem" : "Nova Mensagem"
    clientMessageId.value = messageId || ""
    const message = clientMessages.find((item) => item.id === messageId) || null
    clientMessageTitle.value = message?.title || ""
    clientMessageContent.value = message?.message || ""
    clientMessageAttachment.value = message?.attachment || ""
    clientMessageStatus.value = message?.status || "pendente"
    clientMessageModal.hidden = false
    clientMessageTitle.focus()
  }

  async function deleteClientMessage(messageId) {
    if (!confirm("Tem certeza que deseja excluir esta mensagem?")) return
    try {
      const response = await fetch(`/api/clients/${clientAuth.id}/messages/${messageId}`, { method: "DELETE" })
      if (!response.ok) throw new Error("Erro ao excluir mensagem")
      await loadClientMessages()
    } catch (error) {
      alert("Não foi possível excluir a mensagem.")
    }
  }

  clientNewBtn?.addEventListener("click", () => openClientMessageModal())
  clientMessageModalClose?.addEventListener("click", closeClientMessageModal)
  clientMessageModalCancel?.addEventListener("click", closeClientMessageModal)
  clientMessageModal?.addEventListener("click", (e) => {
    if (e.target === clientMessageModal) closeClientMessageModal()
  })

  clientMessageForm?.addEventListener("submit", async (e) => {
    e.preventDefault()
    const payload = {
      title: clientMessageTitle.value.trim(),
      message: clientMessageContent.value.trim(),
      attachment: clientMessageAttachment.value.trim() || null,
      status: clientMessageStatus.value,
    }

    const messageId = clientMessageId.value
    try {
      const response = await fetch(`/api/clients/${clientAuth.id}/messages${messageId ? `/${messageId}` : ""}`, {
        method: messageId ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
      if (!response.ok) throw new Error("Erro ao salvar mensagem")
      clientMessageForm.reset()
      closeClientMessageModal()
      await loadClientMessages()
    } catch (error) {
      alert("Não foi possível salvar a mensagem.")
    }
  })

  function parseServerError(errorData) {
    const raw = errorData?.detail
    if (Array.isArray(raw)) {
      return raw.map((e) => e.msg || "erro de validação").join("; ")
    }
    if (typeof raw === "string" && raw) return raw
    return "erro desconhecido no servidor"
  }

  clientLoginSubmitBtn?.addEventListener("click", async () => {
    const email = clientEmailInput.value.trim()
    const password = clientPasswordInput.value.trim()
    if (!email || !password) {
      clientLoginError.textContent = "Preencha e-mail e senha."
      clientLoginError.hidden = false
      return
    }

    try {
      const response = await fetch("/api/clients/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      })
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "credenciais inválidas" }))
        throw new Error(parseServerError(errorData))
      }
      clientAuth = await response.json()
      localStorage.setItem("markosdev_client_auth", JSON.stringify(clientAuth))
      setClientAreaLoggedIn(true)
      await loadClientMessages()
    } catch (error) {
      clientLoginError.textContent = error.message || "Não foi possível fazer login."
      clientLoginError.hidden = false
    }
  })

  clientPasswordInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") clientLoginSubmitBtn.click()
  })

  clientLogoutBtn?.addEventListener("click", () => {
    setClientAreaLoggedIn(false)
  })

  const storedClientAuth = localStorage.getItem("markosdev_client_auth")
  if (storedClientAuth) {
    try {
      clientAuth = JSON.parse(storedClientAuth)
      setClientAreaLoggedIn(true)
      loadClientMessages()
    } catch {
      localStorage.removeItem("markosdev_client_auth")
      setClientAreaLoggedIn(false)
    }
  } else {
    setClientAreaLoggedIn(false)
  }

  /* ---------- SPA Hash-based Switching ---------- */
  const navItems = document.querySelectorAll(".nav-item")
  const sections = document.querySelectorAll(".section")
  const searchInput = document.getElementById("search-input")
  const searchButton = document.getElementById("search-btn")
  const searchButtonMobile = document.getElementById("search-btn-mobile")
  const searchEmpty = document.getElementById("search-empty")
  let currentSearchTerm = ""

  function resetSearchState() {
    sections.forEach((section) => {
      section.classList.remove("search-match", "search-hide")
    })
    if (searchEmpty) {
      searchEmpty.hidden = true
      searchEmpty.textContent = ""
    }
    if (searchInput) {
      searchInput.value = ""
    }
    currentSearchTerm = ""
  }

  function handleNavigation() {
    resetSearchState()

    let hash = window.location.hash
    // Default to #inicio if hash is empty or doesn't match an existing section
    if (!hash || !document.querySelector(hash)) {
      hash = "#inicio"
    }

    // Toggle active classes on sections
    sections.forEach((section) => {
      if (`#${section.id}` === hash) {
        section.classList.add("active")
      } else {
        section.classList.remove("active")
      }
    })

    // Toggle active classes on nav sidebar items
    navItems.forEach((item) => {
      const href = item.getAttribute("href")
      if (href === hash) {
        item.classList.add("active")
      } else {
        item.classList.remove("active")
      }
    })

    // Scroll window back to top when switching tab
    window.scrollTo({ top: 0, behavior: "instant" })
  }

  // Listen to hash changes in window
  window.addEventListener("hashchange", handleNavigation)
  // Execute navigation on initial page load
  handleNavigation()

  function applySearch(query) {
    const term = query.trim().toLowerCase()
    const activeSectionId = document.querySelector(".section.active")?.id
    let hasMatch = false

    if (!term) {
      resetSearchState()
      return
    }

    sections.forEach((section) => {
      const sectionText = section.textContent.toLowerCase()
      const isActiveSection = section.id === activeSectionId
      const matches = sectionText.includes(term) || isActiveSection

      section.classList.toggle("search-match", matches)
      section.classList.toggle("search-hide", !matches)

      if (matches) hasMatch = true
    })

    if (searchEmpty) {
      searchEmpty.hidden = hasMatch
      searchEmpty.textContent = hasMatch
        ? ""
        : `Nenhum resultado encontrado para "${query.trim()}".`
    }
  }

  function triggerSearch() {
    currentSearchTerm = searchInput?.value || ""
    applySearch(currentSearchTerm)
  }

  searchInput?.addEventListener("input", (event) => {
    currentSearchTerm = event.target.value
  })

  searchInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault()
      triggerSearch()
    }
  })

  searchButton?.addEventListener("click", triggerSearch)
  searchButtonMobile?.addEventListener("click", triggerSearch)

  applySearch("")

  /* ---------- Rodapé: ano dinâmico ---------- */
  document.getElementById("copyright").textContent =
    `© ${new Date().getFullYear()} MarkosDev. Todos os direitos reservados.`

  /* ---------- Chat Widget ---------- */
  const chatToggle = document.getElementById("chat-toggle")
  const chatWindow = document.getElementById("chat-window")
  const chatClose = document.getElementById("chat-close")
  const chatFabIcon = document.getElementById("chat-fab-icon")
  const chatMessages = document.getElementById("chat-messages")
  const chatForm = document.getElementById("chat-form")
  const chatInput = document.getElementById("chat-input")

  const messages = [
    { from: "bot", text: "Olá! Sou o assistente de IA do MarkosDev. Como posso ajudar?" },
    { from: "user", text: "Quais tecnologias você domina?" },
    { from: "bot", text: "Trabalho com Python, FastAPI, Docker e deploy na Oracle Cloud." },
  ]

  function renderMessages() {
    chatMessages.innerHTML = ""
    messages.forEach((msg) => {
      const row = document.createElement("div")
      row.className = `msg-row ${msg.from}`
      const bubble = document.createElement("p")
      bubble.className = "msg-bubble"
      bubble.textContent = msg.text
      row.appendChild(bubble)
      chatMessages.appendChild(row)
    })
    chatMessages.scrollTop = chatMessages.scrollHeight
  }
  renderMessages()

  function setChat(open) {
    chatWindow.hidden = !open
    chatFabIcon.setAttribute("data-lucide", open ? "x" : "message-square")
    chatToggle.setAttribute("aria-label", open ? "Fechar chat" : "Abrir chat")
    if (typeof lucide !== "undefined") lucide.createIcons()
    if (open) chatInput.focus()
  }

  chatToggle.addEventListener("click", () => setChat(chatWindow.hidden))
  chatClose.addEventListener("click", () => setChat(false))

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault()
    const text = chatInput.value.trim()
    if (!text) return

    messages.push({ from: "user", text })
    chatInput.value = ""
    renderMessages()

    const botMessage = { from: "bot", text: "Digitando..." }
    messages.push(botMessage)
    renderMessages()

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      })

      // Se o servidor retornou erro HTTP
      if (!response.ok) {
        const errData = await response.json().catch(() => ({ detail: "Erro ao conectar com o assistente." }))
        botMessage.text = errData.detail || "Erro ao conectar com o assistente."
        renderMessages()
        return
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ""
      botMessage.text = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split("\n")
        buffer = lines.pop()

        for (const line of lines) {
          if (line.startsWith("data:")) {
            const data = line.slice(5).trim()
            if (data === "[DONE]") break
            try {
              const parsed = JSON.parse(data)
              if (parsed.content) {
                botMessage.text += parsed.content
                renderMessages()
              }
            } catch (err) { /* ignore parse errors */ }
          }
        }
      }
    } catch (err) {
      botMessage.text = "Desculpe, ocorreu um erro ao conectar com o assistente."
      renderMessages()
    }
  })

  /* ---------- Blog ---------- */
  const blogSection = document.getElementById("blog")
  const blogList = document.getElementById("blog-list")
  const blogFeatured = document.getElementById("blog-featured")
  const blogPrev = document.getElementById("blog-prev")
  const blogNext = document.getElementById("blog-next")
  const blogAll = document.getElementById("blog-all")

  const blogColors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6"]
  const blogPageSize = 5
  let blogPage = 0
  let blogTotal = 0
  let blogItems = []
  let blogShowAll = false

  function formatDateTime(iso) {
    const date = new Date(iso)
    if (Number.isNaN(date.getTime())) return iso
    return new Intl.DateTimeFormat("pt-BR", {
      dateStyle: "long",
      timeStyle: "short",
    }).format(date)
  }

  function renderFeatured(news) {
    const imageHtml = news.image_url
      ? `<img src="${news.image_url}" alt="${news.title}" class="blog-featured-image" loading="lazy" />`
      : ""

    blogFeatured.innerHTML = `
      ${imageHtml}
      <div class="blog-featured-meta">
        <h3 class="blog-featured-title">${news.title}</h3>
        <time class="blog-featured-date" datetime="${news.published_at}">${formatDateTime(news.published_at)}</time>
      </div>
      <div class="blog-featured-content">${news.content.replace(/\n/g, "<br>")}</div>
    `
  }

  function renderBlogList(items) {
    blogList.innerHTML = ""
    items.forEach((item, index) => {
      const li = document.createElement("li")
      li.className = "blog-list-item"
      const itemNumber = blogShowAll ? index + 1 : blogPage * blogPageSize + index + 1
      li.innerHTML = `
        <span class="blog-list-number" style="color: ${blogColors[index % blogColors.length]}">${itemNumber}</span>
        <button class="blog-list-button" type="button" data-id="${item.id}">${item.title}</button>
      `
      blogList.appendChild(li)
    })

    blogList.querySelectorAll(".blog-list-button").forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = Number(btn.dataset.id)
        const selected = blogItems.find((n) => n.id === id)
        if (selected) renderFeatured(selected)
      })
    })
  }

  function updateBlogIndex() {
    blogPrev.disabled = blogShowAll || blogPage <= 0
    blogNext.disabled = blogShowAll || (blogPage + 1) * blogPageSize >= blogTotal
    blogAll.textContent = blogShowAll ? "Voltar para a navegação" : "Ver todas as notícias"
  }

  async function loadBlogPage(page = 0, showAll = false) {
    try {
      const skip = showAll ? 0 : page * blogPageSize
      const limit = showAll ? 1000 : blogPageSize
      const [newsRes, countRes] = await Promise.all([
        fetch(`/api/news?skip=${skip}&limit=${limit}`),
        fetch("/api/news/count"),
      ])

      if (!newsRes.ok || !countRes.ok) throw new Error("Erro ao carregar notícias")

      const countData = await countRes.json()
      blogItems = await newsRes.json()
      blogTotal = showAll ? blogItems.length : countData.total
      blogPage = showAll ? 0 : page
      blogShowAll = showAll

      renderBlogList(blogItems)
      updateBlogIndex()

      if (blogItems.length > 0) {
        const selected = blogItems.find((item) => item.id === blogItems[0].id) || blogItems[0]
        renderFeatured(selected)
      } else {
        blogFeatured.innerHTML = `<p class="blog-empty">Nenhuma notícia encontrada.</p>`
      }
    } catch (err) {
      blogFeatured.innerHTML = `<p class="blog-empty">Não foi possível carregar as notícias.</p>`
      console.error(err)
    }
  }

  function initBlog() {
    if (!blogSection || !blogList) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && blogItems.length === 0) {
            loadBlogPage(0)
          }
        })
      },
      { threshold: 0.1 }
    )
    observer.observe(blogSection)

    blogPrev.addEventListener("click", () => {
      if (!blogShowAll && blogPage > 0) loadBlogPage(blogPage - 1)
    })

    blogNext.addEventListener("click", () => {
      if (!blogShowAll && (blogPage + 1) * blogPageSize < blogTotal) loadBlogPage(blogPage + 1)
    })

    blogAll.addEventListener("click", () => {
      if (blogShowAll) {
        loadBlogPage(0, false)
      } else {
        loadBlogPage(0, true)
      }
    })
  }

  initBlog()

  /* ---------- Formulário de contato ---------- */
  const contactForm = document.querySelector(".contact-form")
  const submitBtn = contactForm?.querySelector("button[type='submit']")

  contactForm?.addEventListener("submit", async (e) => {
    e.preventDefault()
    if (!submitBtn) return

    const formData = new FormData(contactForm)
    const payload = {
      name: formData.get("name"),
      email: formData.get("email"),
      subject: formData.get("subject"),
      message: formData.get("message"),
    }

    const originalText = submitBtn.textContent
    submitBtn.disabled = true
    submitBtn.textContent = "Enviando..."

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Erro ao enviar mensagem." }))
        throw new Error(error.detail || "Erro ao enviar mensagem.")
      }

      alert("Mensagem enviada com sucesso! Entrarei em contato em breve.")
      contactForm.reset()
    } catch (err) {
      alert(err.message || "Não foi possível enviar a mensagem. Tente novamente mais tarde.")
    } finally {
      submitBtn.disabled = false
      submitBtn.textContent = originalText
    }
  })

  /* ---------- Renderiza ícones lucide ---------- */
  if (typeof lucide !== "undefined") lucide.createIcons()
})

/* ============================================
   Painel Administrativo
============================================ */
document.addEventListener("DOMContentLoaded", () => {
  const ADMIN_PASSWORD_KEY = "markosdev_admin_token"

  // Elementos
  const loginSection = document.getElementById("admin-login")
  const dashboardSection = document.getElementById("admin-dashboard")
  const passwordInput = document.getElementById("admin-password")
  const loginBtn = document.getElementById("admin-login-btn")
  const loginError = document.getElementById("admin-login-error")
  const newsList = document.getElementById("admin-news-list")
  const newBtn = document.getElementById("admin-new-btn")
  const modal = document.getElementById("admin-modal")
  const modalClose = document.getElementById("admin-modal-close")
  const modalCancel = document.getElementById("admin-modal-cancel")
  const modalForm = document.getElementById("admin-modal-form")
  const modalTitle = document.getElementById("admin-modal-title")
  const editId = document.getElementById("admin-edit-id")
  const editTitle = document.getElementById("admin-edit-title")
  const editContent = document.getElementById("admin-edit-content")
  const editImage = document.getElementById("admin-edit-image")
  const editActiveGroup = document.getElementById("admin-edit-active-group")
  const editActive = document.getElementById("admin-edit-active")

  let adminToken = localStorage.getItem(ADMIN_PASSWORD_KEY) || ""

  function getHeaders() {
    return {
      "Content-Type": "application/json",
      "x-admin-password": adminToken,
    }
  }

  // Verificar se já está autenticado ao carregar
  if (adminToken) {
    verifyAndLoad()
  }

  // Login
  loginBtn.addEventListener("click", async () => {
    const password = passwordInput.value.trim()
    if (!password) {
      loginError.textContent = "Digite a senha."
      loginError.hidden = false
      return
    }

    // Estado de carregamento
    const originalText = loginBtn.innerHTML
    loginBtn.disabled = true
    loginBtn.innerHTML = '<i data-lucide="loader"></i> Entrando...'
    if (typeof lucide !== "undefined") lucide.createIcons()

    try {
      const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      })

      if (!res.ok) {
        loginError.textContent = "Senha inválida. Tente novamente."
        loginError.hidden = false
        return
      }

      loginError.hidden = true
      adminToken = password
      localStorage.setItem(ADMIN_PASSWORD_KEY, password)
      passwordInput.value = ""
      showDashboard()
    } catch (err) {
      loginError.textContent = "Erro de conexão com o servidor."
      loginError.hidden = false
    } finally {
      loginBtn.disabled = false
      loginBtn.innerHTML = originalText
      if (typeof lucide !== "undefined") lucide.createIcons()
    }
  })

  passwordInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") loginBtn.click()
  })

  async function verifyAndLoad() {
    try {
      const res = await fetch("/api/admin/news", {
        headers: getHeaders(),
      })
      if (res.ok) {
        showDashboard()
      } else {
        localStorage.removeItem(ADMIN_PASSWORD_KEY)
        adminToken = ""
      }
    } catch {
      localStorage.removeItem(ADMIN_PASSWORD_KEY)
      adminToken = ""
    }
  }

  function showDashboard() {
    loginSection.hidden = true
    dashboardSection.hidden = false
    loadNews()
  }

  // Carregar notícias
  async function loadNews() {
    try {
      const res = await fetch("/api/admin/news", { headers: getHeaders() })
      if (!res.ok) throw new Error("Falha ao carregar")

      const news = await res.json()
      renderNewsList(news)
    } catch (err) {
      newsList.innerHTML = `<p class="admin-empty">Erro ao carregar notícias.</p>`
    }
  }

  function renderNewsList(news) {
    if (news.length === 0) {
      newsList.innerHTML = `<p class="admin-empty">Nenhuma notícia cadastrada. Clique em "Nova Notícia" para criar.</p>`
      return
    }

    newsList.innerHTML = ""
    news.forEach((item) => {
      const div = document.createElement("div")
      div.className = "admin-news-item"

      const status = item.is_active ? "" : " [Inativa]"
      const date = new Date(item.published_at).toLocaleDateString("pt-BR")

      div.innerHTML = `
        <div class="admin-news-info">
          <div class="admin-news-title">${item.title}${status}</div>
          <div class="admin-news-meta">${date} · ID: ${item.id}</div>
        </div>
        <div class="admin-news-actions">
          <button class="icon-btn edit-btn" data-id="${item.id}" aria-label="Editar">
            <i data-lucide="pencil"></i>
          </button>
          <button class="icon-btn delete-btn" data-id="${item.id}" aria-label="Excluir">
            <i data-lucide="trash-2"></i>
          </button>
        </div>
      `

      newsList.appendChild(div)
    })

    if (typeof lucide !== "undefined") lucide.createIcons()

    // Eventos de editar
    newsList.querySelectorAll(".edit-btn").forEach((btn) => {
      btn.addEventListener("click", () => openEdit(Number(btn.dataset.id)))
    })

    // Eventos de excluir
    newsList.querySelectorAll(".delete-btn").forEach((btn) => {
      btn.addEventListener("click", () => confirmDelete(Number(btn.dataset.id)))
    })
  }

  // Nova notícia
  newBtn.addEventListener("click", () => openNew())

  function openNew() {
    modalTitle.textContent = "Nova Notícia"
    editId.value = ""
    editTitle.value = ""
    editContent.value = ""
    editImage.value = ""
    editActiveGroup.hidden = true
    modal.hidden = false
  }

  async function openEdit(id) {
    try {
      const res = await fetch(`/api/admin/news/${id}`, { headers: getHeaders() })
      if (!res.ok) throw new Error("Erro ao carregar notícia")

      const news = await res.json()
      modalTitle.textContent = "Editar Notícia"
      editId.value = news.id
      editTitle.value = news.title
      editContent.value = news.content
      editImage.value = news.image_url || ""
      editActiveGroup.hidden = false
      editActive.checked = news.is_active
      modal.hidden = false
    } catch (err) {
      alert("Erro ao carregar notícia para edição.")
    }
  }

  // Fechar modal
  function closeModal() {
    modal.hidden = true
  }

  modalClose.addEventListener("click", closeModal)
  modalCancel.addEventListener("click", closeModal)
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal()
  })

  // Salvar (criar ou atualizar)
  modalForm.addEventListener("submit", async (e) => {
    e.preventDefault()

    const id = editId.value
    const title = editTitle.value.trim()
    const content = editContent.value.trim()
    const image_url = editImage.value.trim() || null
    const is_active = editActive.checked

    const saveBtn = document.getElementById("admin-modal-save")
    const originalText = saveBtn.innerHTML
    saveBtn.disabled = true
    saveBtn.innerHTML = "Salvando..."

    try {
      if (id) {
        // Atualizar
        const body = { title, content, image_url, is_active }
        const res = await fetch(`/api/admin/news/${id}`, {
          method: "PUT",
          headers: getHeaders(),
          body: JSON.stringify(body),
        })
        if (!res.ok) throw new Error("Erro ao atualizar")
      } else {
        // Criar
        const body = { title, content, image_url }
        const res = await fetch("/api/admin/news", {
          method: "POST",
          headers: getHeaders(),
          body: JSON.stringify(body),
        })
        if (!res.ok) throw new Error("Erro ao criar")
      }

      closeModal()
      loadNews()
    } catch (err) {
      alert("Erro ao salvar notícia.")
    } finally {
      saveBtn.disabled = false
      saveBtn.innerHTML = originalText
    }
  })

  // Excluir
  async function confirmDelete(id) {
    if (!confirm("Tem certeza que deseja excluir esta notícia?")) return

    try {
      const res = await fetch(`/api/admin/news/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      })
      if (!res.ok) throw new Error("Erro ao excluir")

      loadNews()
    } catch (err) {
      alert("Erro ao excluir notícia.")
    }
  }
})
