<template>
  <v-menu
    v-model="dropdown"
    bottom
    offset-x
    open-on-hover
    :open-on-click="false"
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ on }">
      <v-btn
        v-long-press="500"
        color="success"
        text
        v-on="on"
        @long-press-start="dropdown = true"
        @mouseup="doneButtonClicked(maintenanceObject.maintenance_id)"
      >
        Done!
      </v-btn>
    </template>
    <v-list v-on-clickaway="clickAway">
      <v-list-item-group
        v-model="selected_chips_array"
        multiple
        active-class="success--text"
      >
        <template
          v-for="(item, index) in maintenance_chips"
        >
          <v-list-item
            :key="maintenanceObject.maintenance_id + '/done-modifier/' + index"
          >
            <v-list-item-content>
              <v-list-item-title>{{ item }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list-item-group>
    </v-list>
  </v-menu>
</template>

<script>
import LongPress from 'vue-directive-long-press';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  name: 'MaintenanceTableDropdown',
  directives: {
    'long-press': LongPress,
    onClickaway,
  },
  props: {
    maintenanceObject: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    dropdown: false,
    maintenance_chips: ['checked', 'fixed', 'replaced'],
    selected_chips_array: [],
  }),
  created() {
    this.selected_chips_array = this.getDefaultTags();
  },
  updated() {
  },
  methods: {
    /**
     * Gets the default tags for a maintenance item.
     * @returns {array} array of the default tags
     */
    getDefaultTags() {
      const tagsDefault = this.maintenanceObject.tags_default;
      const selectedChipsArray = [];
      if (tagsDefault.includes('checked')) {
        selectedChipsArray.push(0);
      }
      if (tagsDefault.includes('fixed')) {
        selectedChipsArray.push(1);
      }
      if (tagsDefault.includes('replaced')) {
        selectedChipsArray.push(2);
      }
      return selectedChipsArray;
    },
    /**
     * Closes the dropdown if clicked anywhere else.
     */
    clickAway() {
      this.dropdown = false;
    },
    /**
     * Emits a message to the parent component that the done button was clicked and parses the
     * maintenance id.
     * @param {string} mtnId maintenance id
     */
    doneButtonClicked(mtnId) {
      const selectedChips = this.chipNumberToString();
      this.$emit('doneButtonClicked', mtnId, selectedChips);
      setTimeout(() => {
        this.dropdown = false;
      }, 1);
    },
    /**
     * The selected maintenance tag chips are encoded as numbers, translates these numbers back to
     * the corresponding string.
     * @returns {array} array of maintenance tags
     */
    chipNumberToString() {
      const selectedChipsArray = [];
      if (this.selected_chips_array.includes(0)) {
        selectedChipsArray.push('checked');
      }
      if (this.selected_chips_array.includes(1)) {
        selectedChipsArray.push('fixed');
      }
      if (this.selected_chips_array.includes(2)) {
        selectedChipsArray.push('replaced');
      }
      return selectedChipsArray;
    },
  },
};
</script>

<style scoped>

</style>
