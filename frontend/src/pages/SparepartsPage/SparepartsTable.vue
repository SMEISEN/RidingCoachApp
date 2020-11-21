<template>
  <v-data-table
    :headers="headers"
    :items="desserts"
    :search="spareparts_search"
  />
</template>

<script>
export default {
  name: 'SparepartsTable',
  props: {
    sparepartsSearch: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    headers: [
      {
        text: 'Part',
        align: 'start',
        sortable: false,
        value: 'name',
      },
      {
        text: 'Stock',
        align: 'start',
        sortable: false,
        value: 'current_stock',
      },
      {
        text: 'Warn at',
        align: 'start',
        sortable: false,
        value: 'min_stock',
      },
    ],
    desserts: [],
    search: [],
  }),
  computed: {
    spareparts_search: {
      get() {
        return this.sparepartsSearch;
      },
      set(value) {
        this.$emit('update:sparepartsSearch', value);
      },
    },
  },
};
</script>

<style scoped>

</style>
