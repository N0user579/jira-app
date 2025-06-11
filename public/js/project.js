// Project-specific JavaScript
let projectKey = ""
let projectName = ""
let users = []
let currentGenerationType = ""

// Initialize project page
document.addEventListener("DOMContentLoaded", () => {
  // Get project info from URL parameters
  const urlParams = new URLSearchParams(window.location.search)
  projectKey = urlParams.get("key")
  projectName = urlParams.get("name") || projectKey

  if (!projectKey) {
    alert("Project key not found")
    window.location.href = "/"
    return
  }

  // Update page elements
  document.getElementById("projectName").textContent = projectName
  document.getElementById("projectKey").textContent = projectKey

  // Load project data
  loadUsers()
  loadIssues()
})

// Load users for the project
async function loadUsers() {
  try {
    const response = await fetch(`/api/users?project=${projectKey}`)
    users = await response.json()

    // Populate user dropdowns
    const storyAssignee = document.getElementById("storyAssignee")
    const epicAssignee = document.getElementById("epicAssignee")

    users.forEach((user) => {
      const option1 = document.createElement("option")
      option1.value = user.accountId
      option1.textContent = user.displayName
      storyAssignee.appendChild(option1)

      const option2 = document.createElement("option")
      option2.value = user.accountId
      option2.textContent = user.displayName
      epicAssignee.appendChild(option2)
    })
  } catch (error) {
    console.error("Error loading users:", error)
  }
}

// Load recent issues
async function loadIssues() {
  try {
    const response = await fetch(`/api/issues?project=${projectKey}`)
    const data = await response.json()
    const issues = data.issues || []

    const issuesList = document.getElementById("issuesList")

    if (issues.length === 0) {
      issuesList.innerHTML = '<div class="empty-state"><p>No issues found</p></div>'
      return
    }

    issuesList.innerHTML = ""

    issues.slice(0, 10).forEach((issue) => {
      const issueItem = document.createElement("div")
      issueItem.className = "issue-item"

      const iconClass = issue.fields.issuetype.name === "Epic" ? "flag" : "bookmark"
      const assigneeName = issue.fields.assignee ? issue.fields.assignee.displayName : "Unassigned"

      issueItem.innerHTML = `
                <div class="issue-type">
                    <i class="fas fa-${iconClass}"></i>
                    ${issue.fields.issuetype.name}
                </div>
                <div class="issue-summary">
                    <strong>${issue.key}</strong>: ${issue.fields.summary}
                </div>
                <div class="issue-meta">
                    <span class="status">${issue.fields.status.name}</span>
                    <span class="assignee">${assigneeName}</span>
                </div>
            `

      issuesList.appendChild(issueItem)
    })
  } catch (error) {
    console.error("Error loading issues:", error)
    document.getElementById("issuesList").innerHTML = '<div class="error">Error loading issues</div>'
  }
}

// AI Generation functions
function showStoryGenerator() {
  currentGenerationType = "story"
  document.getElementById("aiGenerator").style.display = "block"
  document.getElementById("aiInput").placeholder = "Describe the user requirements and functionality needed..."
  document.getElementById("aiContext").placeholder = "Additional context about the user, system, or business goals..."
}

function showEpicGenerator() {
  currentGenerationType = "epic"
  document.getElementById("aiGenerator").style.display = "block"
  document.getElementById("aiInput").placeholder = "Describe the epic theme or high-level feature..."
  document.getElementById("aiContext").placeholder = "Business objectives and success criteria..."
}

function showLoading(button, text) {
  button.disabled = true
  button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`
}

function hideLoading(button, originalText) {
  button.disabled = false
  button.innerHTML = originalText
}

function openModal(modalId) {
  $(`#${modalId}`).modal("show")
}

function closeModal(modalId) {
  $(`#${modalId}`).modal("hide")
}

// Generate content with AI
document.getElementById("generateBtn").addEventListener("click", async function () {
  const input = document.getElementById("aiInput").value
  const context = document.getElementById("aiContext").value
  const resultDiv = document.getElementById("aiResult")

  if (!input.trim()) {
    alert("Please provide requirements or theme")
    return
  }

  const originalText = this.innerHTML
  showLoading(this, "Generating...")
  resultDiv.innerHTML = ""

  try {
    const endpoint = currentGenerationType === "story" ? "/api/generate-story" : "/api/generate-epic"
    const payload =
      currentGenerationType === "story"
        ? { requirements: input, context: context }
        : { theme: input, objectives: context }

    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })

    const data = await response.json()

    if (response.ok) {
      resultDiv.innerHTML = `<div class="generated-content">${data.content.replace(/\n/g, "<br>")}</div>`

      // Add button to use generated content
      const useBtn = document.createElement("button")
      useBtn.className = "btn btn-success"
      useBtn.innerHTML = '<i class="fas fa-check"></i> Use This Content'
      useBtn.onclick = () => useGeneratedContent(data.content)
      resultDiv.appendChild(useBtn)
    } else {
      resultDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`
  }

  hideLoading(this, originalText)
})

// Use generated content
function useGeneratedContent(content) {
  if (currentGenerationType === "story") {
    openModal("storyModal")
    // Parse and fill the story form
    const lines = content.split("\n")
    const summary = lines.find((line) => line.includes("As a")) || "Generated User Story"
    document.getElementById("storySummary").value = summary.replace(/^\d+\.\s*/, "")
    document.getElementById("storyDescription").value = content
  } else {
    openModal("epicModal")
    // Parse and fill the epic form
    const lines = content.split("\n")
    const title = lines[0] || "Generated Epic"
    document.getElementById("epicSummary").value = title.replace(/^\d+\.\s*/, "")
    document.getElementById("epicDescription").value = content
  }
}

// Form submissions
document.getElementById("storyForm").addEventListener("submit", async (e) => {
  e.preventDefault()
  await createIssue("Story", "storyModal")
})

document.getElementById("epicForm").addEventListener("submit", async (e) => {
  e.preventDefault()
  await createIssue("Epic", "epicModal")
})

// Create issue in Jira
async function createIssue(type, modalId) {
  const isStory = type === "Story"
  const summary = document.getElementById(isStory ? "storySummary" : "epicSummary").value
  const description = document.getElementById(isStory ? "storyDescription" : "epicDescription").value
  const assignee = document.getElementById(isStory ? "storyAssignee" : "epicAssignee").value

  try {
    const response = await fetch("/api/create-issue", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project_key: projectKey,
        issue_type: type,
        summary: summary,
        description: description,
        assignee: assignee || null,
      }),
    })

    const result = await response.json()

    if (result.success) {
      alert(`${type} created successfully: ${result.issue_key}`)
      closeModal(modalId)
      loadIssues() // Refresh issues list
    } else {
      alert(`Error creating ${type}: ${result.error}`)
    }
  } catch (error) {
    alert(`Error: ${error.message}`)
  }
}
