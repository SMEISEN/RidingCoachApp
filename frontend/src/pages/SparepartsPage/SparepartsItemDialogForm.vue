<template>
  <v-edit-dialog
    :return-value.sync="sparepartItem.sparepart_id"
    large
    persistent
    @save="onSave(sparepartItem.sparepart_id)"
    @cancel="onCancel"
  >
    <v-badge
      v-if="sparepartItem.current_stock < sparepartItem.min_stock"
      color="red"
      dot
    >
      {{ sparepartItem.current_stock }}
    </v-badge>
    <span v-else>
      {{ sparepartItem.current_stock }}
    </span>
    <template v-slot:input>
      <SparepartsItemTable
        :sparepart-child.sync="spareparts_child"
        :sparepart-child-template="spareparts_child_template"
      />
    </template>
  </v-edit-dialog>
</template>

<script>
import SparepartsItemTable from './SparepartsItemTable.vue';

export default {
  name: 'SparepartsItemDialogForm',
  components: {
    SparepartsItemTable,
  },
  props: {
    sparepartItem: {
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
  computed: {
    spareparts_child: {
      get() {
        return this.sparepartChild;
      },
      set(value) {
        this.$emit('update:sparepartChild', value);
      },
    },
    spareparts_child_template() {
      return this.sparepartChildTemplate;
    },
  },
  methods: {
    /**
     * Emits a message to the parent component that the save button was clicked and parses the
     * spare part id.
     * @param {string} sparepartId id of the spare part
     */
    onSave(sparepartId) {
      this.$emit('addSparepartItems', sparepartId);
    },
    /**
     * Emits a message to the parent component that the cancel button was clicked.
     */
    onCancel() {
      this.$emit('initForm');
    },
  },
};
</script>

<style scoped>

</style>
