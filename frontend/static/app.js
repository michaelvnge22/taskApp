// frontend/static/app.js
const API_URL = "http://127.0.0.1:8000";

async function api(method, url, body = null, auth = true) {
    const headers = { "Content-Type": "application/json" };
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

    if (res.status === 401) {
        localStorage.removeItem("token");
        window.location = "login.html";
        return;
    }

    return res;
}

// AUTH
async function loginUser(email, password) {
    const res = await api("POST", "/auth/login", { email, password }, false);
    return res.json();
}
async function registerUser(username, email, password) {
    const res = await api("POST", "/auth/register", { username, email, password }, false);
    return res.json();
}

// GROUPS
async function fetchGroups() {
    const res = await api("GET", "/groups/");
    return res ? res.json() : [];
}
async function createGroup(name) {
    const res = await api("POST", "/groups/", { name });
    return res ? res.json() : null;
}
async function fetchGroup(id) {
    const res = await api("GET", `/groups/${id}`);
    return res ? res.json() : null;
}
async function fetchGroupMembers(id) {
    const res = await api("GET", `/groups/${id}/members`);
    return res ? res.json() : [];
}
async function generateInvite(groupId) {
    const res = await api("POST", `/groups/${groupId}/invite`);
    return res ? res.json() : null;
}
async function removeMember(groupId, userId) {
    const res = await api("DELETE", `/groups/${groupId}/members/${userId}`);
    return res ? res.json() : null;
}
async function joinGroupByToken(token) {
    const res = await api("GET", `/groups/join/${token}`);
    return res ? res.json() : null;
}

// TASKS
async function fetchGroupTasks(groupId) {
    const res = await api("GET", `/tasks/group/${groupId}`);
    return res ? res.json() : [];
}
async function createTask(groupId, title, description = "", deadline = null, status = "todo") {
    const body = {
        title,
        description,
        deadline,
        status,
        group_id: Number(groupId)
    };
    const res = await api("POST", `/tasks/`, body);
    return res ? res.json() : null;
}
async function updateTask(taskId, data) {
    const res = await api("PUT", `/tasks/${taskId}`, data);
    return res ? res.json() : null;
}
async function deleteTask(taskId) {
    const res = await api("DELETE", `/tasks/${taskId}`);
    return res ? res.json() : null;
}

// LOGOUT
function logout() {
    localStorage.removeItem("token");
    window.location = "login.html";
}
