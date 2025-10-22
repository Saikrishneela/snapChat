document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const bitmojiImage = document.getElementById("bitmojiImage");

    profileIcon.addEventListener("click", () => {
        bitmojiImage.classList.toggle("hidden");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const updates = document.getElementById("update");
    const storyHide = document.getElementById("dropdown");
    storyHide.addEventListener("click", () => {
        updates.classList.toggle("hidden")
    });

});
document.addEventListener("DOMContentLoaded", () => {
    const addBtn = document.getElementById("addBtn");
    const chatList = document.getElementById("chatList");

    // Load all chats
    async function loadChats() {
        const response = await fetch("/get-chats/");
        const chats = await response.json();

        chatList.innerHTML = ""; // Clear existing chats

        chats.forEach(chat => {
            const newChat = document.createElement("div");
            newChat.classList.add("chat-item");

            newChat.innerHTML = `
                <div class="chat-icon">${chat.emoji}</div>
                <div class="chat-info">
                    <div class="chat-name">${chat.name}</div>
                    <div class="chat-time">${chat.time}</div>
                    <button class="add-friend"><sup>+Add</sup></button>
                </div>
            `;
            chatList.appendChild(newChat);
        });
    }

    // Load pending friend requests
    async function loadPendingRequests() {
        const response = await fetch("/pending-requests/");
        const requests = await response.json();

        chatList.innerHTML = ""; // Clear chat list

        if (requests.length === 0) {
            chatList.innerHTML = `<p style="text-align:center; color:gray;">No pending requests</p>`;
            return;
        }

        requests.forEach(req => {
            const newReq = document.createElement("div");
            newReq.classList.add("chat-item");

            newReq.innerHTML = `
                <div class="chat-icon">📩</div>
                <div class="chat-info">
                    <div class="chat-name">${req.sender}</div>
                    <div class="chat-time">New Request</div>
                    <button class="accept-friend"><sup>Accept</sup></button>
                </div>
            `;
            chatList.appendChild(newReq);
        });
    }

    // Add a new random chat (top + button)
    addBtn.addEventListener("click", async () => {
        const response = await fetch("/add-chat/", { method: "POST" });
        const result = await response.json();

        if (result.success) {
            loadChats(); // Reload chats so the new one appears
        }
    });

    // Handle friend request (+Add) and accept request buttons
    document.addEventListener("click", async (e) => {
        // Send friend request
        if (e.target.classList.contains("add-friend")) {
            const receiver = e.target.closest(".chat-info").querySelector(".chat-name").textContent;

            const formData = new FormData();
            formData.append("receiver", receiver);

            const response = await fetch("/send-request/", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert(`Friend request sent to ${receiver}`);
                e.target.disabled = true;
                e.target.textContent = "✔ Sent";
            } else {
                alert(result.error || "Something went wrong");
            }
        }

        // Accept friend request
        if (e.target.classList.contains("accept-friend")) {
            const sender = e.target.closest(".chat-info").querySelector(".chat-name").textContent;

            const formData = new FormData();
            formData.append("sender", sender);

            const response = await fetch("/accept-request/", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert(result.message);
                e.target.disabled = true;
                e.target.textContent = "✔ Accepted";

                // Reload chats to show new friend
                loadChats();
            } else {
                alert(result.error || "Something went wrong");
            }
        }
    });

    // Toggle tabs between Chats and Requests
    document.getElementById("chatsTab").addEventListener("click", () => {
        document.getElementById("chatsTab").classList.add("active-tab");
        document.getElementById("requestsTab").classList.remove("active-tab");
        loadChats();
    });

    document.getElementById("requestsTab").addEventListener("click", () => {
        document.getElementById("requestsTab").classList.add("active-tab");
        document.getElementById("chatsTab").classList.remove("active-tab");
        loadPendingRequests();
    });

    // Initial load
    loadChats();
});
