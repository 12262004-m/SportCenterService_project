<template>
  <div class="add-sportsman-form">
    <form @submit.prevent="addSportsmen">
      <div class="form-row">
        <div class="form-group">
          <label for="first_name">Имя</label>
          <input type="text" id="first_name" v-model="newSportsman.firstName" required />
        </div>
        <div class="form-group">
          <label for="last_name">Фамилия</label>
          <input type="text" id="last_name" v-model="newSportsman.lastName" required />
        </div>
        <div class="form-group">
          <label for="middle_name">Отчество</label>
          <input type="text" id="middle_name" v-model="newSportsman.middleName" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="gender">Пол</label>
          <select id="gender" v-model="newSportsman.gender" required>
            <option value="MALE">Мужской</option>
            <option value="FEMALE">Женский</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date_of_birth">Дата рождения</label>
          <input type="date" id="date_of_birth" v-model="newSportsman.dateOfBirth" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="phone_number">Телефон</label>
          <input type="tel" id="phone_number" v-model="newSportsman.phoneNumber" required />
        </div>
        <div class="form-group">
          <label for="email">Почта</label>
          <input type="email" id="email" v-model="newSportsman.email" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="registration_date">Дата зачисления</label>
          <input type="date" id="registration_date" v-model="newSportsman.registrationDate" required />
        </div>
      </div>
      <button type="submit">Добавить ученика</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newSportsman: {
        firstName: "",
        lastName: "",
        middleName: "",
        gender: "MALE",
        dateOfBirth: "",
        phoneNumber: "",
        email: "",
        registrationDate: "",
      },
    };
  },
  methods: {
    async addSportsmen() {
      const mutation = `
    mutation CreateSportsman(
      $lastName: String!,
      $firstName: String!,
      $middleName: String!,
      $gender: GenderEnum!,
      $dateOfBirth: Date!,
      $phoneNumber: String!,
      $email: String!,
      $registrationDate: Date!
    ) {
      createSportsman(
        lastName: $lastName,
        firstName: $firstName,
        middleName: $middleName,
        gender: $gender,
        dateOfBirth: $dateOfBirth,
        phoneNumber: $phoneNumber,
        email: $email,
        registrationDate: $registrationDate
      ) {
        id
        lastName
        firstName
        middleName
      }
    }
  `;

      const variables = {
        lastName: this.newSportsman.lastName,
        firstName: this.newSportsman.firstName,
        middleName: this.newSportsman.middleName,
        gender: this.newSportsman.gender.toUpperCase(),
        dateOfBirth: this.newSportsman.dateOfBirth.trim(),
        phoneNumber: this.newSportsman.phoneNumber,
        email: this.newSportsman.email,
        registrationDate: this.newSportsman.registrationDate.trim(),
      };

      try {
        console.log(variables)
        const response = await fetch("http://localhost:8000/graphql/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: mutation, variables }),
        });

        const result = await response.json();

        if (result.errors) {
          console.error(result.errors);
          alert("Ошибка при добавлении спортсмена");
          return;
        }

        alert("Спортсмен успешно добавлен!");
        this.clearForm();
      } catch (error) {
        alert("Ошибка: " + error.message);
      }
    },
    clearForm() {
      this.newSportsman = {
        firstName: "",
        lastName: "",
        middleName: "",
        gender: "MALE",
        dateOfBirth: "",
        phoneNumber: "",
        email: "",
        registrationDate: "",
      };
    },
  },
};
</script>

<style scoped>

.add-sportsman-form {
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  border: 1px solid #ddd;
}

h5 {
  color: #1F2937;
  text-align: center;
}

.form-row {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 100px;
}

label {
  display: block;
  font-weight: bold;
}

input,
select,
button {
  width: 100%;
  padding: 5px;
  margin: 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #3771f3;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #213e83;
}
</style>
