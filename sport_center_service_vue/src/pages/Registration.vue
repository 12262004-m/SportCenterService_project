<template>
  <div class="register-container">
    <div class="register-card">
      <h3 class="register-title">Регистрация</h3>
      <form @submit.prevent="register" class="register-form">
        <input
            type="text"
            v-model="username"
            id="username"
            class="register-input"
            placeholder="Имя пользователя"
            required
        />

        <input
            type="email"
            v-model="email"
            id="email"
            class="register-input"
            placeholder="Email"
            required
        />

        <input
            type="password"
            v-model="password"
            id="password"
            class="register-input"
            placeholder="Пароль"
            required
        />

        <input
            type="password"
            v-model="confirmPassword"
            id="confirmPassword"
            class="register-input"
            placeholder="Подтвердите пароль"
            required
        />

        <button type="submit" class="register-button">Зарегистрироваться</button>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    async register() {
      try {
        if (this.password !== this.confirmPassword) {
          alert("Пароли не совпадают");
          return;
        }
        const query = `
        mutation {
        createUser(
          username: "${this.username}",
          email: "${this.email}",
          password: "${this.password}"
        ) {
          id
          username
          email
          }
        }
      `;

        const response = await fetch("http://localhost:8000/graphql", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ query })
        });

        const result = await response.json();

        if (result.errors) {
          console.error("GraphQL ошибка:", result.errors);
          alert("Ошибка при регистрации: " + result.errors[0].message);
          return;
        }

        alert("Регистрация прошла успешно!");
        this.$router.push("/login");
      } catch (error) {
        console.error("Ошибка:", error);
        alert("Ошибка при регистрации");
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.register-card {
  background: #ffffff;
  padding: 2%;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

.register-title {
  font-weight: bold;
  color: #1F2937;
  margin-bottom: 5%;
  text-align: center;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.register-input {
  padding: 10px;
  border: 1px solid #3771f3;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.register-input:focus {
  border-color: #213e83;
  outline: none;
}

.register-button {
  padding: 10px;
  color: white;
  background-color: #3771f3;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
}

.register-button:hover {
  background-color: #213e83;
}
</style>
