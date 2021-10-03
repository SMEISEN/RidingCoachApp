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
        <td>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <span
                v-bind="attrs"
                v-on="on"
              >
                {{ item.compound }}
              </span>
            </template>
            <span>
              {{ item.manufacturer + ' ' + item.name  + ' ' + item.dimension }}
            </span>
          </v-tooltip>
        </td>
        <td>{{ item.dot }}</td>
        <td>{{ item.operating_hours + ' h' }}</td>
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