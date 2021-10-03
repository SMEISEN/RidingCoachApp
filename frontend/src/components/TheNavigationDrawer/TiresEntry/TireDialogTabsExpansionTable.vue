<template>
  <v-simple-table>
    <thead>
    <tr>
        <th />
        <th />
        <th />
    </tr>
    </thead>
    <tbody>
    <tr
        v-for="item in tireArray"
        :key="item.tire_id"
    >
        <td>{{ item.compound }}</td>
        <td>{{ item.dot }}</td>
        <td>{{ item.operating_hours }}</td>
    </tr>
    </tbody>
  </v-simple-table>
</template>

<script>

export default {
  name: 'TireDialogTabsExpansionTable',
  components: {
  },
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    tire_panel: [0,1],
  }),
};
</script>

<style scoped>

</style>