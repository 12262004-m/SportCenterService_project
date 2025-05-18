<template>
  <div class="add-coach-form">
    <form @submit.prevent="addCoach">
      <div class="form-row">
        <div class="form-group">
          <label for="first_name">Имя</label>
          <input type="text" id="first_name" v-model="newCoach.firstName" required />
        </div>
        <div class="form-group">
          <label for="last_name">Фамилия</label>
          <input type="text" id="last_name" v-model="newCoach.lastName" required />
        </div>
        <div class="form-group">
          <label for="middle_name">Отчество</label>
          <input type="text" id="middle_name" v-model="newCoach.middleName" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="gender">Пол</label>
          <select id="gender" v-model="newCoach.gender" required>
            <option value="MALE">Мужской</option>
            <option value="FEMALE">Женский</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date_of_birth">Дата рождения</label>
          <input type="date" id="date_of_birth" v-model="newCoach.dateOfBirth" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="qualification">Квалификация</label>
          <input type="text" id="qualification" v-model="newCoach.qualification" required />
        </div>
        <div class="form-group">
          <label for="experience">Опыт работы</label>
          <input type="number" id="experience" v-model="newCoach.experience" required />
        </div>
      </div>
      <button type="submit">Добавить тренера</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newCoach: {
        firstName: "",
        lastName: "",
        middleName: "",
        gender: "MALE",
        dateOfBirth: "",
        qualification: "",
        experience: ""
      },
    };
  },
  methods: {
    async addCoach() {
      const mutation = `
        mutation CreateCoach(
        $lastName: String!,
        $firstName: String!,
        $middleName: String!,
        $gender: GenderEnum!,
        $dateOfBirth: Date!,
        $qualification: String!,
        $experience: Int!
      ) {
          createCoach(
            lastName: $lastName,
            firstName: $firstName,
            middleName: $middleName,
            gender: $gender,
            dateOfBirth: $dateOfBirth,
            qualification: $qualification,
            experience: $experience
          ) {
            id
            lastName
            firstName
            middleName
          }
        }
      `;
      const variables = {
        lastName: this.newCoach.lastName,
        firstName: this.newCoach.firstName,
        middleName: this.newCoach.middleName,
        gender: this.newCoach.gender.toUpperCase(),
        dateOfBirth: this.newCoach.dateOfBirth.trim(),
        qualification: this.newCoach.qualification,
        experience: this.newCoach.experience,
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
          alert("Ошибка при добавлении тренера");
          return;
        }
        alert("Тренер успешно добавлен");
        this.clearForm();
      } catch (error) {
        alert("Ошибка: " + error.message);
      }
    },
    clearForm() {
      this.newCoach = {
        firstName: "",
        lastName: "",
        middleName: "",
        gender: "MALE",
        dateOfBirth: "",
        qualification: "",
        experience: ""
      };
    },
  },
};
</script>

<style scoped>

.add-coach-form {
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
