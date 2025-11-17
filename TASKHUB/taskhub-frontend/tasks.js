document.addEventListener("DOMContentLoaded", () => {
    
    // --- Configuração e Verificação ---
    
    const API_URL = "http://127.0.0.1:5000"; // Porta correta
    const token = localStorage.getItem("token");

    // Se não há token, redireciona para login
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    // --- Elementos do DOM ---
    const taskList = document.getElementById("task-list");
    const logoutBtn = document.getElementById("logout-btn");
    const modal = document.getElementById("task-modal");
    const addTaskBtn = document.getElementById("add-task-btn");
    const closeBtn = document.querySelector(".close-btn");
    const taskForm = document.getElementById("task-form");
    const modalTitle = document.getElementById("modal-title");
    const modalError = document.getElementById("modal-error");
    const taskIdInput = document.getElementById("task-id");
    const titleInput = document.getElementById("title");
    const descriptionInput = document.getElementById("description");
    const priorityInput = document.getElementById("priority");
    const statusInput = document.getElementById("status");

    // Verifica elementos essenciais
    if (!taskList || !logoutBtn || !modal || !addTaskBtn || !taskForm) {
        console.error("Elementos DOM necessários não encontrados. Verifique o HTML.");
        return;
    }

    // --- Funções Principais ---

    async function fetchTasks() {
        try {
            console.log("Buscando tarefas com token:", token);
            const response = await fetch(`${API_URL}/tasks`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (response.status === 401) {
                logout();
                return;
            }

            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }

            const tasks = await response.json();
            renderTasks(tasks);
        } catch (error) {
            console.error("Erro ao buscar tarefas:", error);
            taskList.innerHTML = "<p>Não foi possível carregar as tarefas. Verifique a conexão.</p>";
        }
    }

    function renderTasks(tasks) {
        taskList.innerHTML = "";
        
        if (tasks.length === 0) {
            taskList.innerHTML = "<p>Você ainda não tem tarefas.</p>";
            return;
        }

        tasks.forEach(task => {
            const taskElement = document.createElement("div");
            taskElement.className = `task-item ${task.status.toLowerCase().replace(' ', '-')}`;
            taskElement.innerHTML = `
                <div class="task-info">
                    <h3>${task.title}</h3>
                    <p>${task.description || 'Sem descrição'}</p>
                    <span class="badge priority-${task.priority.toLowerCase()}">${task.priority}</span>
                    <span class="badge status-${task.status.toLowerCase().replace(' ', '-')}">${task.status}</span>
                </div>
                <div class="task-actions">
                    <button class="btn-icon edit-btn" data-id="${task.id}">Editar</button>
                    <button class="btn-icon delete-btn" data-id="${task.id}">Excluir</button>
                </div>
            `;
            
            taskElement.querySelector(".edit-btn").addEventListener("click", () => openEditModal(task));
            taskElement.querySelector(".delete-btn").addEventListener("click", () => deleteTask(task.id));

            taskList.appendChild(taskElement);
        });
    }

    // === CORREÇÃO PRINCIPAL: handleFormSubmit (linha ~118) ===
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        const taskId = taskIdInput.value;
        const isEditing = !!taskId;
        const method = isEditing ? "PUT" : "POST";
        const url = isEditing ? `${API_URL}/tasks/${taskId}` : `${API_URL}/tasks`;

        // Monta payload com validação
        const payload = {
            title: titleInput.value.trim(),
            description: descriptionInput.value.trim() || null, // null se vazio
            priority: priorityInput.value,
            status: statusInput.value
        };

        // Validações
        if (!payload.title) {
            modalError.textContent = "Título é obrigatório.";
            return;
        }

        const validPriorities = ["Baixa", "Média", "Alta"];
        const validStatuses = ["Pendente", "Em Andamento", "Concluída"];

        if (!validPriorities.includes(payload.priority)) {
            modalError.textContent = "Selecione uma prioridade válida.";
            return;
        }

        if (!validStatuses.includes(payload.status)) {
            modalError.textContent = "Selecione um status válido.";
            return;
        }

        try {
            console.log(`Salvando tarefa (${method}):`, payload);

            const response = await fetch(url, {
                method: method,
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            console.log("Resposta:", response.status);

            if (!response.ok) {
                let errorMsg = "Erro ao salvar tarefa.";
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.message || errorMsg;
                } catch {}
                modalError.textContent = errorMsg;
                return;
            }

            closeModal();
            fetchTasks();
        } catch (error) {
            console.error("Erro de rede:", error);
            modalError.textContent = "Erro de conexão com o servidor.";
        }
    }

    async function deleteTask(taskId) {
        if (!confirm("Tem certeza que deseja excluir esta tarefa?")) return;

        try {
            const response = await fetch(`${API_URL}/tasks/${taskId}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (!response.ok) {
                alert("Erro ao excluir tarefa.");
                return;
            }
            
            fetchTasks();
        } catch (error) {
            console.error("Erro ao excluir:", error);
            alert("Erro de conexão.");
        }
    }

    // --- Modal ---
    function openAddModal() {
        modalTitle.textContent = "Nova Tarefa";
        taskForm.reset();
        taskIdInput.value = "";
        modalError.textContent = "";
        modal.style.display = "block";
    }

    function openEditModal(task) {
        modalTitle.textContent = "Editar Tarefa";
        modalError.textContent = "";
        taskIdInput.value = task.id;
        titleInput.value = task.title;
        descriptionInput.value = task.description || "";
        priorityInput.value = task.priority;
        statusInput.value = task.status;
        modal.style.display = "block";
    }

    function closeModal() {
        modal.style.display = "none";
    }

    function logout() {
        localStorage.removeItem("token");
        window.location.href = "login.html";
    }

    // --- Event Listeners ---
    logoutBtn.addEventListener("click", logout);
    addTaskBtn.addEventListener("click", openAddModal);
    closeBtn.addEventListener("click", closeModal);
    taskForm.addEventListener("submit", handleFormSubmit);

    window.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });

    // --- Inicialização ---
    fetchTasks();
});