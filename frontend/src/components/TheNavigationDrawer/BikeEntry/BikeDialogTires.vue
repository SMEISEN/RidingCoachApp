<template>
  <v-menu
    v-model="tire_menu"
    :close-on-content-click="false"
    transition="scale-transition"
    :nudge-right="40"
    offset-y
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        v-model="display_pressure_steps"
        label="Pressure"
        hint="bar"
        readonly
        v-on="on"
      />
    </template>
    <v-card>
      <v-card-text>
        <LineChart
          v-if="tire_pressure_dialog_array.length > 0"
          :chart-data="data_collection"
          :options="data_options"
          :height="null"
          :width="null"
        />
        <v-simple-table>
          <thead>
            <tr>
              <th
                class="text-left"
                style="min-width: 125px;width: 125px;max-width: 125px"
              >
                Temperature
              </th>
              <th
                class="text-left"
                style="min-width: 125px;width: 125px;max-width: 125px"
              >
                Pressure
              </th>
              <th />
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(entry, index) in tire_pressure_dialog_array"
              :key="entry.temperature + entry.pressure"
            >
              <td style="border-bottom: none">
                <v-text-field
                  v-model.number="entry.temperature"
                  append-outer-icon="mdi-plus"
                  prepend-icon="mdi-minus"
                  style="font-size: 12px"
                  hint="°C"
                  dense
                  height="20px"
                  single-line
                  @click:append-outer.prevent="
                    entry.temperature = incrementTemperature(entry.temperature)"
                  @click:prepend.prevent="
                    entry.temperature = decrementTemperature(entry.temperature)"
                />
              </td>
              <td style="border-bottom: none">
                <v-text-field
                  v-model.number="entry.pressure"
                  append-outer-icon="mdi-plus"
                  prepend-icon="mdi-minus"
                  :rules="[v => v >= 0]"
                  style="font-size: 12px"
                  hint="bar"
                  dense
                  height="20px"
                  single-line
                  @click:append-outer.prevent="
                    entry.pressure = incrementPressure(entry.pressure)"
                  @click:prepend.prevent="
                    entry.pressure = decrementPressure(entry.pressure)"
                />
              </td>
              <td style="border-bottom: none">
                <v-btn
                  icon
                  @click="deleteSetupRow(index)"
                >
                  <v-icon>
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-card-text>
      <v-card>
        <v-btn
          absolute
          x-small
          fab
          top
          left
          color="primary"
          @click.prevent="addSetupRow"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-card>
      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          color="primary"
          @click="cancelInput"
        >
          Cancel
        </v-btn>
        <v-btn
          text
          color="primary"
          @click="saveInput"
        >
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'pressure entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed"
    />
  </v-menu>
</template>

<script>
import {
  mean,
  min,
  max,
} from 'mathjs';
import {
  decrementNumber,
  incrementNumber,
} from '../../utils/FromUtils';
import LineChart from '../../common/LineChart.vue';
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog.vue';

export default {
  name: 'BikeDialogTires',
  components: {
    LineChart,
    ConfirmDeleteDialog,
  },
  props: {
    tirePressureArray: {
      type: Array,
      default: () => [this.tire_pressure_template],
    },
  },
  data: () => ({
    tire_menu: false,
    tire_pressure_dialog_array: [],
    tire_pressure_template: {
      temperature: null,
      pressure: null,
    },
    row_to_be_deleted: null,
    confirm_delete_dialog: false,
    data_collection: {
      datasets: [],
    },
    data_sets: [
      {
        data: [],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '',
        pointBackgroundColor: '',
      },
    ],
    data_options: {
      responsive: true,
      aspectRatio: 2,
      maintainAspectRatio: true,
      animation: false,
      title: {
        display: false,
        text: 'Weather Data',
      },
      legend: {
        display: false,
      },
      scales: {
        xAxes: [
          {
            type: 'linear',
            ticks: {
              source: 'labels',
              fontSize: 10,
            },
            gridLines: {
              color: [],
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              fontSize: 10,
            },
          },
        ],
      },
    },
  }),
  computed: {
    tire_pressure_array: {
      get() {
        return this.tirePressureArray;
      },
      set(value) {
        this.$emit('update:tirePressureArray', value);
      },
    },
    display_pressure_steps() {
      let displayString = '';
      if (this.tire_pressure_array.length > 0) {
        const tirePressure = this.tire_pressure_array.map((value) => value.pressure);
        const tirePressureMean = mean(tirePressure).toFixed(2);
        const tirePressureHalfRange = (
          (max(tirePressure) - min(tirePressure)) / 2.0
        ).toFixed(2);
        displayString = `${tirePressureMean} ± ${tirePressureHalfRange}`;
      }
      return displayString;
    },
  },
  watch: {
    tire_pressure_dialog_array: {
      deep: true,
      handler() {
        this.data_sets[0].pointBackgroundColor = this.$vuetify.theme.themes.light.info;
        this.data_sets[0].borderColor = this.$vuetify.theme.themes.light.accent;
        this.data_sets[0].data = [];
        for (let i = 0; i < this.tire_pressure_dialog_array.length; i += 1) {
          this.data_sets[0].data.push({
            x: this.tire_pressure_dialog_array[i].temperature,
            y: this.tire_pressure_dialog_array[i].pressure,
          });
        }
        this.$set(this.data_collection, 'datasets', this._.cloneDeep(this.data_sets));
      },
    },
  },
  created() {
    this.tire_pressure_dialog_array = this._.cloneDeep(this.tire_pressure_array);
    if (this.tire_pressure_dialog_array.length === 0) {
      this.addSetupRow();
    }
  },
  methods: {
    addSetupRow() {
      this.tire_pressure_dialog_array = this.tire_pressure_dialog_array
        .concat(this._.cloneDeep(this.tire_pressure_template));
    },
    deleteSetupRow(index) {
      this.confirm_delete_dialog = true;
      this.row_to_be_deleted = index;
    },
    deletionConfirmed() {
      this.tire_pressure_dialog_array.splice(this.row_to_be_deleted, 1);
      this.row_to_be_deleted = null;
    },
    incrementTemperature(inputNumber) {
      return incrementNumber(inputNumber, 1, 0);
    },
    decrementTemperature(inputNumber) {
      return decrementNumber(inputNumber, 1, 0);
    },
    incrementPressure(inputNumber) {
      return incrementNumber(inputNumber, 0.05, 2);
    },
    decrementPressure(inputNumber) {
      return decrementNumber(inputNumber, 0.05, 2);
    },
    saveInput() {
      this.tire_pressure_array = this._.cloneDeep(this.tire_pressure_dialog_array);
      this.tire_menu = false;
    },
    cancelInput() {
      this.tire_pressure_dialog_array = this._.cloneDeep(this.tire_pressure_array);
      if (this.tire_pressure_dialog_array.length === 0) {
        this.addSetupRow();
      }
      this.tire_menu = false;
    },
  },
};
</script>
