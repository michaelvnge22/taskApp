// -------------------------
// API Helper
// -------------------------
const API_URL = "http://127.0.0.1:8000";

async function api(method, url, body = null, auth = true) {
    const headers = { "Content-Type": "application/json" };

    // include token if needed
    if (auth) {
        const token = localStorage.getItem("token");
        if (!token) {
            window.location = "login.html";
            return;
        }
        headers["Authorization"] = "Bearer " + token;
    }

    const res = await fetch(API_URL + url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
    });

    // token invalid → redirect
    if (res.status === 401) {
        localStorage.removeItem("token");
        window.location = "login.html";
        return;
    }

    return res;
}

// -------------------------
// AUTH
// -------------------------
async function loginUser(email, password) {
    const res = await api("POST", "/auth/login", { email, password }, false);
    return res.json();
}

async function registerUser(username, email, password) {
    const res = await api("POST", "/auth/register", { username, email, password }, false);
    return res.json();
}

// -------------------------
// GROUPS
// -------------------------
async function fetchGroups() {
    return (await api("GET", "/groups/")).json();
}

async function createGroup(name) {
    return (await api("POST", "/groups/", { name })).json();
}

async function fetchGroup(id) {
    return (await api("GET", `/groups/${id}`)).json();
}

async function joinGroupByToken(token) {
    return (await api("GET", `/groups/join/${token}`)).json();
}

// -------------------------
// TASKS
// -------------------------
// 👉 Correction importante : bonne route = /tasks/group/{groupId}
async function fetchGroupTasks(groupId) {
    return (await api("GET", `/tasks/group/${groupId}`)).json();
}

// 👉 Create Task correctly with POST /tasks/
async function createTask(groupId, title, description = "", deadline = null) {
    return (
        await api("POST", `/tasks/`, {
            title,
            description,
            deadline,
            group_id: groupId
        })
    ).json();
}

async function updateTask(taskId, data) {
    return (await api("PUT", `/tasks/${taskId}`, data)).json();
}

async function deleteTask(taskId) {
    return (await api("DELETE", `/tasks/${taskId}`)).json();
}

// -------------------------
// LOGOUT
// -------------------------
function logout() {
    localStorage.removeItem("token");
    window.location = "login.html";
}
