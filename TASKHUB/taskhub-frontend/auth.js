// Espera o DOM carregar para poder adicionar os 'escutadores' de evento
document.addEventListener("DOMContentLoaded", () => {
    
    // Define a URL base da nossa API
    const API_URL = "http://127.0.0.1:5000"; // A URL onde o Back End Flask está rodando

    // Pega os elementos do formulário (com verificações para evitar erros)
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const errorMessage = document.getElementById("error-message");

    // Função auxiliar para mostrar erros (melhorada com console.log para depuração)
    function displayError(message) {
        console.error("Erro:", message); // Log no console para depuração
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = "block"; // Garante que o erro seja visível
        } else {
            alert(message); // Fallback se o elemento não existir
        }
    }

    // --- Lógica de LOGIN ---
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault(); // Impede o envio tradicional do formulário
            
            const email = document.getElementById("email");
            const password = document.getElementById("password");
            
            // Verifica se os campos existem e têm valores
            if (!email || !password) {
                displayError("Campos de email ou senha não encontrados.");
                return;
            }
            
            const emailValue = email.value.trim();
            const passwordValue = password.value.trim();
            
            if (!emailValue || !passwordValue) {
                displayError("Preencha todos os campos.");
                return;
            }
            
            try {
                console.log("Tentando login com:", { email: emailValue }); // Log para depuração
                
                // Faz a chamada (fetch) para o endpoint /auth/login do Back End
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email: emailValue, password: passwordValue })
                });

                const data = await response.json();
                console.log("Resposta da API:", data); // Log da resposta

                if (response.ok) {
                    // Login bem-sucedido!
                    // Salva o token JWT no 'localStorage' do navegador
                    localStorage.setItem("token", data.access_token);
                    
                    // Redireciona para a página principal de tarefas
                    window.location.href = "tasks.html"; 
                } else {
                    // Mostra a mensagem de erro vinda da API
                    displayError(data.message || "Erro ao fazer login. Verifique suas credenciais.");
                }

            } catch (error) {
                console.error("Erro de conexão:", error); // Log detalhado
                displayError("Não foi possível conectar à API. Verifique se o servidor Flask está rodando.");
            }
        });
    } else {
        console.warn("Formulário de login não encontrado nesta página.");
    }

    // --- Lógica de CADASTRO (SIGNUP) ---
    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const name = document.getElementById("name");
            const email = document.getElementById("email");
            const password = document.getElementById("password");
            
            // Verifica se os campos existem e têm valores
            if (!name || !email || !password) {
                displayError("Campos de nome, email ou senha não encontrados.");
                return;
            }
            
            const nameValue = name.value.trim();
            const emailValue = email.value.trim();
            const passwordValue = password.value.trim();
            
            if (!nameValue || !emailValue || !passwordValue) {
                displayError("Preencha todos os campos.");
                return;
            }
            
            try {
                console.log("Tentando cadastro com:", { name: nameValue, email: emailValue }); // Log para depuração
                
                // Faz a chamada para o endpoint /auth/signup do Back End
                const response = await fetch(`${API_URL}/auth/signup`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: nameValue, email: emailValue, password: passwordValue })
                });

                const data = await response.json();
                console.log("Resposta da API:", data); // Log da resposta

                if (response.status === 201) {
                    // Cadastro bem-sucedido!
                    alert("Usuário criado com sucesso! Faça o login.");
                    window.location.href = "login.html"; // Redireciona para o login
                } else {
                    displayError(data.message || "Erro ao cadastrar. Tente novamente.");
                }

            } catch (error) {
                console.error("Erro de conexão:", error); // Log detalhado
                displayError("Não foi possível conectar à API. Verifique se o servidor Flask está rodando.");
            }
        });
    } else {
        console.warn("Formulário de cadastro não encontrado nesta página.");
    }
});
