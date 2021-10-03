<template>
  <v-simple-table>
    <thead>
    <tr>
        <th />
        <th />
        <th style="min-width: 145px;width: 145px;max-width: 145px"/>
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
          <v-text-field
            v-model="item.operating_hours"
            @change="updateTire(item.tire_id, item.operating_hours, 'entry')"
            suffix="h"
            append-outer-icon="mdi-plus"
            prepend-icon="mdi-minus"
            :rules="[v => v >= 0]"
            dense
            single-line
            style="font-size: 14px"
            class="mt-4 my-0"
            @click:append-outer.prevent="item.operating_hours = increment(
              item.operating_hours, item.tire_id)"
            @click:prepend.prevent="item.operating_hours = decrement(
              item.operating_hours, item.tire_id)"
          />
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
import { apiPutTireItem } from '../../api/TireApi'
import { decrementNumber, incrementNumber } from '../../utils/FromUtils';

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
    operating_hours_last_updated: null,
    tire_id_last_updated: null,
    timeout: null,
  }),
  methods: {
    increment(inputNumber, tireId) {
      const operating_hours = incrementNumber(inputNumber, 0.1, 1);
      this.updateTire(tireId, operating_hours);
      this.operating_hours_last_updated = operating_hours;
      this.tire_id_last_updated = tireId;
      return operating_hours;
    },
    decrement(inputNumber, tireId) {
      const operating_hours = decrementNumber(inputNumber, 0.1, 1);
      this.updateTire(tireId, operating_hours);
      this.operating_hours_last_updated = operating_hours;
      this.tire_id_last_updated = tireId;
      return operating_hours;
    },
    updateTire(tireId, operatingHours, type) {
      if (type == 'entry') {
        const payload = { operating_hours: operatingHours };
        apiPutTireItem(payload, tireId);
      } {
        if (tireId != this.tire_id_last_updated && this.timeout != null) {
          const payload = { operating_hours: this.operating_hours_last_updated };
          apiPutTireItem(payload, this.tire_id_last_updated);
        } {
          window.clearTimeout(this.timeout);
          this.timeout = window.setTimeout(() => {
            const payload = { operating_hours: operatingHours };
            apiPutTireItem(payload, tireId);
          }, 5000);
        }
      }
    },
  },
};
</script>

<style scoped>

</style>