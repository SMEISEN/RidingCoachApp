<template>
  <div>
    <v-simple-table
      dense
    >
      <thead>
      <tr>
          <th />
          <th />
          <th />
          <th style="min-width: 145px;width: 145px;max-width: 145px"/>
          <th />
      </tr>
      </thead>
      <tbody>
      <tr
          v-for="item in tire_array"
          :key="item.tire_id"
      >
          <td>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-progress-circular
                  v-bind="attrs"
                  v-on="on"
                  :value=Math.min(...Object.values(item.condition))*100
                  size=26
                  class="mt-n1 my-0"
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
            <v-btn
              icon
              color="warning"
              @click="editTire(item.tire_id)"
            >
              <v-icon>
                mdi-pencil
              </v-icon>
            </v-btn>
            <v-btn
              icon
              color="error"
              @click="deleteTire(item.tire_id)"
            >
              <v-icon>
                mdi-delete
              </v-icon>
            </v-btn>
          </td>
      </tr>
      </tbody>
    </v-simple-table>
    <v-row>
      <v-col
      cols="12"
      class="text-center"
      >
        <v-btn
            icon
            outlined
            color="accent"
            @click="addTire()"
        >
          <v-icon>
              mdi-plus
          </v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <TireDialogTabsExpansionDialog
      :tire-dialog.sync="tire_dialog"
      :task="tire_dialog_task"
      :tire-data-object="tire_data_object"
      :tire-array="tire_array"
      @refreshTires="$emit('refreshTires')"
      @resetTireForm="resetTireForm()"
    />
    <ConfirmDeleteDialog
      :flagged-for-deletion="'tire entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import {
  apiPutTireItem,
  apiDeleteTireItem,
} from '../../api/TireApi'
import { decrementNumber, incrementNumber } from '../../utils/FromUtils';
import TireDialogTabsExpansionDialog from './TireDialogTabsExpansionDialog.vue';
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog.vue';

export default {
  name: 'TireDialogTabsExpansionTable',
  components: {
    TireDialogTabsExpansionDialog,
    ConfirmDeleteDialog,
  },
  props: {
    tireArray: {
      type: Array,
      required: true,
    },
    tireCategory: {
      type: String,
      required: true,
    },
    tireAxis: {
      type: String,
      required: true,
    },
  },
  computed: {
    tire_array() {
      return this.tireArray;
    },
    tire_category() {
      return this.tireCategory;
    },
    tire_axis() {
      return this.tireAxis;
    },
  },
  data: () => ({
    tire_panel: [0,1],
    operating_hours_last_updated: null,
    tire_id_last_updated: null,
    timeout: null,
    tire_dialog: false,
    tire_data_object_template: {
      tire_id: null,
      bike_id: null,
      rim: null,
      category: null,
      manufacturer: null,
      name: null,
      compound: null,
      axis: null,
      dimension: null,
      dot: null,
      condition: {
        left_outer: 1,
        left_middle: 1,
        center: 1,
        right_middle: 1,
        right_outer: 1
      },
      operating_hours: 0.0,
      comment: null,
    },
    tire_data_object: {},
    tire_dialog_task: '',
    tire_to_be_deleted: null,
    confirm_delete_dialog: false,
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
    editTire(tireId) {
      [this.tire_data_object] = this.tire_array.filter((i) => i.tire_id === tireId);
      this.tire_dialog_task = 'Edit'
      this.tire_dialog = true;
    },
    addTire() {
      if (this.tire_array.length > 0) {
        this.tire_data_object = this._.cloneDeep(this.tire_array[this.tire_array.length -1]);
        this.rim = null;
        this.tire_data_object.dot = null;
        this.tire_data_object.condition = {
          left_outer: 1,
          left_middle: 1,
          center: 1,
          right_middle: 1,
          right_outer: 1
        };
        this.tire_data_object.operating_hours = 0.0;
        this.tire_data_object.comment = null;
      } {
        this.tire_data_object = this._.cloneDeep(this.tire_data_object_template);
        this.tire_data_object.category = this.tire_category;
        this.tire_data_object.axis = this.tire_axis;
      }
      this.tire_dialog_task = 'Add'
      this.tire_dialog = true;
    },
    deleteTire(TireId) {
      this.confirm_delete_dialog = true;
      this.tire_to_be_deleted = TireId;
    },
    deletionConfirmed() {
      apiDeleteTireItem(this.tire_to_be_deleted).then((res) => {
        this.$emit('refreshTires');
      });
      this.tire_to_be_deleted = null;
    },
    resetTireForm() {
      this.tire_data_object = this._.cloneDeep(this.tire_data_object_template);
    },
  },
};
</script>

<style scoped>

</style>