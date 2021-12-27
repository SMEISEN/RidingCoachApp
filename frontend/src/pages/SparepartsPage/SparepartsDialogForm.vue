<template>
  <v-dialog
    v-model="spareparts_dialog"
    persistent
    max-width="500px"
  >
    <v-form
      v-if="spareparts_dialog"
      ref="validation_form"
      v-model="valid"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Add spare part</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model.number="sparepart_parent.name"
                :rules="[v => !!v]"
                label="Name*"
                required
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-select
                v-model.number="sparepart_parent.module"
                :items="bikeModules"
                :rules="[v => !!v]"
                label="Module*"
                required
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="12"
            >
              <v-text-field
                v-model.number="sparepart_parent.min_stock"
                label="Warn at stock"
              />
            </v-col>
          </v-row>
          <SparepartsItemTable
            :sparepart-child.sync="sparepart_child"
            :sparepart-child-template="sparepart_child_template"
          />
          <v-spacer />
          <p class="text--secondary text-sm-right">
            *indicates required field
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="secondary"
            text
            @click.prevent="onCancel"
          >
            Close
          </v-btn>
          <v-btn
            color="secondary"
            :disabled="!valid"
            text
            @click.prevent="onSave"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import SparepartsItemTable from './SparepartsItemTable.vue';

export default {
  name: 'SparepartsDialogForm',
  components: {
    SparepartsItemTable,
  },
  props: {
    sparepartsDialog: {
      type: Boolean,
      required: true,
    },
    bikeModules: {
      type: Array,
      required: true,
    },
    sparepartParent: {
      type: Object,
      required: true,
    },
    sparepartChild: {
      type: Array,
      required: true,
    },
    sparepartChildTemplate: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    valid: true,
  }),
  computed: {
    spareparts_dialog: {
      get() {
        return this.sparepartsDialog;
      },
      set(value) {
        this.$emit('update:sparepartsDialog', value);
      },
    },
    sparepart_parent: {
      get() {
        return this.sparepartParent;
      },
      set(value) {
        this.$emit('update:sparepartParent', value);
      },
    },
    sparepart_child: {
      get() {
        return this.sparepartChild;
      },
      set(value) {
        this.$emit('update:sparepartChild', value);
      },
    },
    sparepart_child_template() {
      return this.sparepartChildTemplate;
    },
  },
  methods: {
    /**
     * Emits a message to the parent component that the save button was clicked and closes the
     * add spare part dialog.
     */
    onSave() {
      this.$emit('addSparepart');
      this.spareparts_dialog = false;
    },
    /**
     * Emits a message to the parent component that the cancel button was clicked, resets the
     * validation of the add spare part dialog form and closes the dialog.
     */
    onCancel() {
      this.$emit('initForm');
      if (typeof this.$refs.validation_form !== 'undefined') {
        this.$refs.validation_form.resetValidation();
      }
      this.spareparts_dialog = false;
    },
  },
};
</script>
