<template>
  <v-edit-dialog
    :return-value.sync="sparepartItem.sparepart_id"
    large
    persistent
    @save="onSave(sparepartItem.sparepart_id)"
    @cancel="onCancel"
  >
    {{ sparepartItem.current_stock }}
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
    onSave(sparepartId) {
      this.$emit('addSparepartItems', sparepartId);
    },
    onCancel() {
      this.$emit('initForm');
    },
  },
};
</script>

<style scoped>

</style>
