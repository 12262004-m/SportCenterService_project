<template>
  <div class="login-container">
    <div class="login-card">
      <h3 class="login-title">Вход в аккаунт</h3>
      <form @submit.prevent="login" class="login-form">
        <input
            type="text"
            v-model="userEmail"
            id="userEmail"
            class="login-input"
            placeholder="Почта"
        />

        <input
            type="password"
            v-model="password"
            id="password"
            class="login-input"
            placeholder="Пароль"
        />

        <button type="submit" class="login-button">Войти</button>
      </form>
      <button class="auth-link" @click="goToRegister">Регистрация</button>
    </div>
  </div>
</template>
<script>
import auth from '../store/auth';

export default {
  data() {
    return {
      userEmail: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const query = `
          mutation Login($userEmail: String!, $password: String!) {
          login(userEmail: $userEmail, password: $password) {
          accessToken
        }
      }
    `;
        const variables = {
          userEmail: this.userEmail,
          password: this.password,
        };
        console.log(variables)

        const response = await fetch("http://127.0.0.1:8000/graphql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query, variables }),
        });
        const result = await response.json();
        if (result.errors) throw new Error(result.errors[0].message);
        const token = result.data.login.access_token;
        auth.login(token);
        this.$router.push("/");
      } catch (error) {
        alert(error.message);
      }
    },
    goToRegister() {
      this.$router.push('/register');
    }
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  background: #ffffff;
  padding: 2%;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-weight: bold;
  color: #1F2937;
  margin-bottom: 5%;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.login-input {
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.login-input:focus {
  border-color: #213e83;
  outline: none;
}

.login-button {
  padding: 10px;
  color: white;
  background-color: #3771f3;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
}

.login-button:hover {
  background-color: #213e83;
}

.auth-link {
  margin-top: 20%;
  padding: 10px;
  color: white;
  background-color: #3771f3;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  width: 100%;
}

.auth-link:hover {
  background-color: #213e83;
}
</style>
