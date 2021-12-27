<template>
    <v-expansion-panels
        v-model="tire_panel"
        multiple
    >
        <v-expansion-panel>
        <v-expansion-panel-header>Front</v-expansion-panel-header>
            <v-expansion-panel-content>
            <TireDialogTabsExpansionTable
                :tire-array="tires_front"
                :tire-dialog.sync="tire_dialog"
                :tire-axis="'Front'"
                :tire-category="tire_category"
                @refreshTires="$emit('refreshTires')"
            />
            </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
        <v-expansion-panel-header>Rear</v-expansion-panel-header>
            <v-expansion-panel-content>
            <TireDialogTabsExpansionTable
                :tire-array="tires_rear"
                :tire-dialog.sync="tire_dialog"
                :tire-axis="'Rear'"
                :tire-category="tire_category"
                @refreshTires="$emit('refreshTires')"
            />
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
import TireDialogTabsExpansionTable from './TireDialogTabsExpansionTable.vue';

export default {
  name: 'TireDialogTabsExpansion',
  components: {
      TireDialogTabsExpansionTable,
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
  },
  computed: {
    tires_front() {
        return this.tireArray.filter((i) => i.axis === 'Front');
    },
    tires_rear() {
        return this.tireArray.filter((i) => i.axis === 'Rear');
    },
    tire_category() {
        return this.tireCategory;
    },
  },
  data: () => ({
    tire_panel: [0,1],
    tire_dialog: false,
  }),
};
</script>
