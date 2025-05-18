<template>
  <div class="main">
    <h2>Секции спортивной школы олимпийского резерва №1</h2>
    <div v-for="section in sections" :key="section.id" class="section-info">
      <div class="section-details">
        <div class="section-full-information">
          <h4>{{ section.title }} </h4>
          <p>Описание: {{ section.description }}</p>
          <p>Тренер: {{ section.coach ? section.coach : "Нет тренера" }}</p>
          <p>Свободных мест: {{ section.capacity - section.sportsmen.length }}</p>
        </div>
        <hr>
        <div class="section-sportsmen">
          <strong>Спортсмены:</strong>
          <ol>
            <li v-for="sportsman in section.sportsmen" :key="sportsman.id">
              <div class="sportsman-item">
                <span>{{ sportsman.lastName }} {{ sportsman.firstName }} {{ sportsman.middleName }} {{ "(" + sportsman.dateOfBirth + ")" }}</span>
                <button @click="removeSportsmanFromSection(section.id, sportsman.id)">Удалить</button>
              </div>
            </li>
            <li v-if="section.sportsmen.length === 0">Нет спортсменов в этой секции.</li>
          </ol>
          <div v-if="section.capacity - section.sportsmen.length > 0">
            <label for="sportsman">Добавить спортсмена: </label>
            <select v-model="selectedSportsman[section.id]">
              <option value="">Выберите спортсмена</option>
              <option v-for="sportsman in sportsmen" :key="sportsman.id" :value="sportsman.id">
                {{ sportsman.lastName }} {{ sportsman.firstName }} {{ sportsman.middleName }}
              </option>
            </select>
            <button @click="addSportsmanToSection(section.id)">
              Добавить
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sections: [],
      sportsmen: [],
      selectedSportsman: {},
    };
  },
  methods: {
    async fetchSections() {
      const query = `
      query {
        getAllSportSections {
        id
        title
        capacity
        description
        sportsmen {
          id
          lastName
          firstName
          middleName
          dateOfBirth
          }
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
        this.sections = result.data.getAllSportSections;
      } catch (error) {
        console.error("Ошибка загрузки секций:", error);
      }
    },

    async fetchSportsmen() {
      const query = `
      query {
        getAllSportsmen{
        id
        lastName
        firstName
        middleName
        dateOfBirth
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
        this.sportsmen = result.data.getAllSportsmen;
      } catch (error) {
        alert("Ошибка загрузки спортсменов:" + error);
      }
    },
    async addSportsmanToSection(sectionId) {
      const sportsmanId = this.selectedSportsman[sectionId];
      if (!sportsmanId) {
        alert("Выберите спортсмена");
        return;
      }
      const section = this.sections.find(s => s.id === sectionId);
      const alreadyAdded = section.sportsmen.some(s => s.id === sportsmanId);
      if (alreadyAdded) {
        alert("Спортсмен уже добавлен в эту секцию");
        return;
      }

      const mutation = `
      query {
        addNewSportsmanToSection(sectionId: ${sectionId}, sportsmanId: ${sportsmanId}) {
          id
          title
          sportsmen {
            id
            lastName
            firstName
            middleName
          }
        }
      }
    `;
      try {
        const response = await fetch('http://localhost:8000/graphql/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: mutation }),
        });

        const result = await response.json();
        if (result.errors) {
          console.error(result.errors);
          alert("Ошибка при добавлении спортсмена");
        } else {
          alert("Спортсмен добавлен");
          this.selectedSportsman[sectionId] = "";
          this.fetchSections();
        }
      } catch (error) {
        alert("Ошибка" + error);
      }
    },
    async removeSportsmanFromSection(sectionId, sportsmanId) {
      console.log(sectionId, sportsmanId)
      const mutation = `
      query {
        deleteSportsmanFromSection(sectionId: ${sectionId}, sportsmanId: ${sportsmanId})
      }
    `;
      try {
        const response = await fetch('http://localhost:8000/graphql/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: mutation }),
        });
        const result = await response.json();

        if (result.data.deleteSportsmanFromSection.includes("успешно")) {
          alert("Спортсмен удалён!");
          this.fetchSections();
        } else {
          alert("Ошибка при удалении спортсмена");
        }
      } catch (error) {
        alert("Ошибка:" + error);
      }
    }
  },
    mounted() {
      this.fetchSections();
      this.fetchSportsmen();
    },
};
</script>


<style scoped>
.main {
  margin: 3%;
}

h2 {
  text-align: center;
  color: #1F2937;
}

h4 {
  color: #3771f3;
}

hr {
  border: none;
  border-left: 2px solid #1F2937;
  margin: 0 20px;
}

.section-info {
  margin-left: auto;
  margin-right: auto;
  padding: 3%;
  margin-top: 2%;
  display: flex;
  border: 2px solid #1F2937;
  border-radius: 20px;
}

.section-details {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.section-full-information {
  flex: 1;
}

.section-sportsmen {
  flex: 0 0 35%;
  padding: 10px;
}

.section-details p {
  color: #555555;
}

label {
  margin-left: 2%;
}

button {
  background-color: #3771f3;
  color: white;
  cursor: pointer;
  width: 100%;
  padding: 5px;
  margin: 2%;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #213e83;
}

.sportsman-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

}

.sportsman-item button {
  background-color: white;
  color: black;
  padding: 4px 8px;
  border: 2px solid #ff565e;
  cursor: pointer;
  font-size: 12px;
  margin-left: 10px;
  max-width: 100px;
  border-radius: 4px;
}

.sportsman-item button:hover {
  background-color: #ffe2e5;
}

</style>

