<template>
  <div class="filter-container">
    <label for="coach-select">Фильтрация по тренеру:</label>
    <select id="coach-select" @change="handleFilter">
      <option value="">Все тренеры</option>
      <option v-for="coach in coaches" :key="coach.id" :value="coach.id">
        {{ coach.lastName }} {{ coach.firstName }} {{ coach.middleName }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    coaches: {
      type: Array,
      required: true,
    },
  },
  methods: {
    handleFilter(event) {
      const selectedCoachId = event.target.value;
      this.$emit("filter-by-coach", selectedCoachId ? Number(selectedCoachId) : null);
    },
  },
};
</script>


<style scoped>
.filter-container {
  margin: 10px 0;
  display: flex;
  align-items: center;
}

label {
  margin-right: 10px;
}

select {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>
