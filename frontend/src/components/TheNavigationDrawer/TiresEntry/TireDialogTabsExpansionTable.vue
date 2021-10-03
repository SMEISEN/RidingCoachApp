<template>
  <v-simple-table>
    <thead>
    <tr>
        <th />
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
        <td>
          {{ item.dot }}
        </td>
        <td>
          {{ item.operating_hours + ' h' }}
        </td>
        <td>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-progress-circular
                v-bind="attrs"
                v-on="on"
                :value=Math.min(...Object.values(item.condition))*100
                size=26
              />
            </template>
            <span>
              {{ 'left outer: ' + item.condition.left_outer * 100 + ' %' }} <br/>
              {{ 'left middle: ' + item.condition.left_middle * 100 + ' %' }} <br/>
              {{ 'center: ' + item.condition.center * 100 + ' %' }} <br/>
              {{ 'right middle: ' + item.condition.right_middle * 100 + ' %' }} <br/>
              {{ 'right outer: ' + item.condition.right_outer * 100 + ' %' }}
            </span>
          </v-tooltip>
        </td>
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