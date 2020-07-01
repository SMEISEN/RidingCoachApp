<template>
  <div>
    <v-subheader>Available setup</v-subheader>
    <v-card-text>
      <v-simple-table dense>
        <thead>
          <tr>
            <th class="text-left">
              Category
            </th>
            <th class="text-left">
              Group
            </th>
            <th class="text-left">
              Name
            </th>
            <th class="text-left">
              Available ticks
            </th>
            <th class="text-left">
              Standard tick
            </th>
            <th class="text-left" />
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(entry, index) in setupIndividual"
            :key="index"
          >
            <td style="border-bottom: none">
              <v-select
                v-model="entry.category"
                :items="['Engine', 'Suspension', 'Electronic']"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.group"
                style="font-size: 12px"
                dense
                height="20px"
                placeholder="default"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.name"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.ticks_available"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
              />
            </td>
            <td style="border-bottom: none">
              <v-text-field
                v-model="entry.ticks_standard"
                style="font-size: 12px"
                dense
                height="20px"
                single-line
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
    <v-card-text style="height: 50px; position: relative">
      <v-btn
        absolute
        small
        fab
        top
        right
        color="primary"
        @click.prevent="addSetupRow"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-card-text>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'setup entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed"
    />
  </div>
</template>

<script>
import ConfirmDeleteDialog from '../../common/ConfirmDeleteDialog.vue';

export default {
  name: 'BikeDialogSetup',
  components: {
    ConfirmDeleteDialog,
  },
  props: {
    bikeFormObject: {
      type: Object,
      required: true,
    },
    setupIndividual: {
      type: Array,
      required: true,
    },
    setupIndividualTemplate: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    confirm_delete_dialog: false,
    row_to_be_deleted: null,
  }),
  updated() {
  },
  created() {
  },
  methods: {
    addSetupRow() {
      this.bikeFormObject.setup_individual.push(this._.cloneDeep(this.setupIndividualTemplate));
    },
    deleteSetupRow(index) {
      this.confirm_delete_dialog = true;
      this.row_to_be_deleted = index;
    },
    deletionConfirmed() {
      this.bikeFormObject.setup_individual.splice(this.row_to_be_deleted, 1);
      this.row_to_be_deleted = null;
    },
  },
};
</script>

<style scoped>

</style>
