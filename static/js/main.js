// Modal functionality
function openModal(modalId) {
  document.getElementById(modalId).style.display = "block"
  document.body.style.overflow = "hidden"
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none"
  document.body.style.overflow = "auto"

  // Reset forms
  const modal = document.getElementById(modalId)
  const forms = modal.querySelectorAll("form")
  forms.forEach((form) => form.reset())

  // Hide AI generator if open
  const aiGenerator = document.getElementById("aiGenerator")
  if (aiGenerator) {
    aiGenerator.style.display = "none"
  }
}

// Close modal when clicking outside
window.onclick = (event) => {
  if (event.target.classList.contains("modal")) {
    const modals = document.querySelectorAll(".modal")
    modals.forEach((modal) => {
      if (modal.style.display === "block") {
        closeModal(modal.id)
      }
    })
  }
}

// Close modal with Escape key
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    const modals = document.querySelectorAll(".modal")
    modals.forEach((modal) => {
      if (modal.style.display === "block") {
        closeModal(modal.id)
      }
    })
  }
})

// Utility functions
function showLoading(element, text = "Loading...") {
  element.disabled = true
  element.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`
}

function hideLoading(element, originalText) {
  element.disabled = false
  element.innerHTML = originalText
}

// Toast notifications
function showToast(message, type = "info") {
  const toast = document.createElement("div")
  toast.className = `toast toast-${type}`
  toast.innerHTML = `
        <i class="fas fa-${type === "success" ? "check" : type === "error" ? "times" : "info"}"></i>
        ${message}
    `

  document.body.appendChild(toast)

  // Show toast
  setTimeout(() => toast.classList.add("show"), 100)

  // Hide toast
  setTimeout(() => {
    toast.classList.remove("show")
    setTimeout(() => document.body.removeChild(toast), 300)
  }, 3000)
}

// Auto-resize textareas
document.addEventListener("DOMContentLoaded", () => {
  const textareas = document.querySelectorAll("textarea")
  textareas.forEach((textarea) => {
    textarea.addEventListener("input", function () {
      this.style.height = "auto"
      this.style.height = this.scrollHeight + "px"
    })
  })
})

// Form validation
function validateForm(formId) {
  const form = document.getElementById(formId)
  const requiredFields = form.querySelectorAll("[required]")
  let isValid = true

  requiredFields.forEach((field) => {
    if (!field.value.trim()) {
      field.style.borderColor = "#e74c3c"
      isValid = false
    } else {
      field.style.borderColor = "#e1e8ed"
    }
  })

  return isValid
}

// Copy to clipboard functionality
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showToast("Copied to clipboard!", "success")
    })
    .catch(() => {
      showToast("Failed to copy to clipboard", "error")
    })
}

// Format date helper
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

// Debounce function for search/filter
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

console.log("Jira BA Assistant loaded successfully!")
