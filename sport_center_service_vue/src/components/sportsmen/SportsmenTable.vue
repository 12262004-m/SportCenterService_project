<template>
  <div>
    <h2>Список всех спортсменов спортивной школы олимпийского резерва №1</h2>
    <table>
      <thead>
      <tr>
        <th>Фамилия</th>
        <th>Имя</th>
        <th>Отчество</th>
        <th>Пол</th>
        <th>Дата рождения</th>
        <th>Номер телефона</th>
        <th>Почта</th>
        <th>Дата зачисления</th>
        <th>Изменения</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="sportsman in sportsmen" :key="sportsman.id">
        <template v-if="sportsman.isEditing">
          <td><input v-model="sportsman.lastName" /></td>
          <td><input v-model="sportsman.firstName" /></td>
          <td><input v-model="sportsman.middleName" /></td>
          <td>
            <select v-model="sportsman.gender">
              <option value="MALE">Мужской</option>
              <option value="FEMALE">Женский</option>
            </select>
          </td>
          <td><input type="date" v-model="sportsman.dateOfBirth" /></td>
          <td><input v-model="sportsman.phoneNumber" /></td>
          <td><input v-model="sportsman.email" /></td>
          <td><input type="date" v-model="sportsman.registrationDate" /></td>
          <td>
            <div class="button-group">
              <button class="button save" @click="saveSportsman(sportsman)">Сохранить</button>
              <button class="button cancel" @click="cancelEdit(sportsman)">Отмена</button>
            </div>
          </td>
        </template>
        <template v-else>
          <td>{{ sportsman.lastName }}</td>
          <td>{{ sportsman.firstName }}</td>
          <td>{{ sportsman.middleName }}</td>
          <td>{{ sportsman.gender === 'MALE' ? 'Мужской' : 'Женский' }}</td>
          <td>{{ sportsman.dateOfBirth }}</td>
          <td>{{ sportsman.phoneNumber }}</td>
          <td>{{ sportsman.email }}</td>
          <td>{{ sportsman.registrationDate }}</td>
          <td>
            <button class="button edit" @click="editSportsman(sportsman)">Редактировать</button>
          </td>
        </template>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sportsmen: [],
      originalSportsmen: {},
    };
  },
  methods: {
    async fetchSportsmen() {
      const query = `
        query {
          getAllSportsmen {
            id
            lastName
            firstName
            middleName
            gender
            dateOfBirth
            phoneNumber
            email
            registrationDate
          }
        }
      `;
      try {
        const response = await fetch('http://localhost:8000/graphql/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({query}),
        });
        const result = await response.json();
        this.sportsmen = result.data.getAllSportsmen.map(s => ({ ...s, isEditing: false }));
      } catch (error) {
        alert("Ошибка загрузки спортсменов:" + error);
      }
    },
    editSportsman(sportsman) {
      this.originalSportsmen[sportsman.id] = { ...sportsman };
      sportsman.isEditing = true;
    },
    cancelEdit(sportsman) {
      Object.assign(sportsman, this.originalSportsmen[sportsman.id]);
      sportsman.isEditing = false;
      delete this.originalSportsmen[sportsman.id];
    },
    async saveSportsman(sportsman) {
      const mutation = `
        mutation UpdateSportsman(
          $sportsmenId: Int!,
          $firstName: String!,
          $lastName: String!,
          $middleName: String!,
          $gender: String!,
          $dateOfBirth: Date!,
          $phoneNumber: String!,
          $email: String!,
          $registrationDate: Date!
        ) {
          updateSportsmen(
            sportsmenId: $sportsmenId,
            firstName: $firstName,
            lastName: $lastName,
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
            gender
            dateOfBirth
            phoneNumber
            email
            registrationDate
          }
        }
      `;

      const variables = {
        sportsmenId: sportsman.id,
        firstName: sportsman.firstName,
        lastName: sportsman.lastName,
        middleName: sportsman.middleName,
        gender: sportsman.gender,
        dateOfBirth: sportsman.dateOfBirth.trim(),
        phoneNumber: sportsman.phoneNumber,
        email: sportsman.email,
        registrationDate: sportsman.registrationDate.trim(),
      };
      try {
        const response = await fetch("http://localhost:8000/graphql/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: mutation, variables }),
        });
        const result = await response.json();
        if (result.errors) {
          console.error(result.errors);
          alert("Ошибка при сохранении: " + result.errors[0].message);
          return;
        }
        const updated = result.data.updateSportsmen;
        Object.assign(sportsman, updated);
        sportsman.isEditing = false;
        delete this.originalSportsmen[sportsman.id];

      } catch (error) {
        alert("Ошибка: " + error.message);
      }
    }
  },
  mounted() {
    this.fetchSportsmen();
  },
};
</script>
<style scoped>
div {
  margin: 3%;
}

h2 {
  text-align: center;
  color: #1F2937;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

table th {
  background-color: #1F2937;
  color: white;
  font-weight: bold;
}

table td {
  background-color: #f8f8f8;
}

table tr:nth-child(even) td {
  background-color: #f4f4f4;
}

table tr:hover {
  background-color: #ddd;
}
.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
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

.button {
  background: white;
  color: black;
  flex: 1;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
}

.button.edit {
  border: 2px solid #ffa44b;
}

.button.edit:hover {
  background: #fbdfb8;
}

.button.save {
  border: 2px solid #005302;
}

.button.save:hover {
  background: #d0fbcd;
}

.button.cancel {
  border: 2px solid #ff565e;
}

.button.cancel:hover {
  background: #ffc8ca;
}
</style>
