<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="sparepart_items"
      :search="spareparts_search"
      :expanded.sync="expanded"
      item-key="name"
      @click:row="expandRow"
    >
      <template v-slot:expanded-item="props">
        <td :colspan="window_width">
          <tr
            v-for="(item) in props.item.items"
            :key="item.sparepartitem_id"
          >
            <td style="min-width: 115px; width: 7000px">
              {{ item.description }}
            </td>
            <td style="min-width: 95px; width: 3000px">
              {{ item.condition }}
            </td>
            <td style="min-width: 75px">
              <v-btn
                color="warning"
                icon
                @click.prevent="onEditButton(item.sparepartitem_id)"
              >
                <v-icon>mdi-square-edit-outline</v-icon>
              </v-btn>
              <v-btn
                color="error"
                icon
                @click.prevent="onDeleteButton(item.sparepartitem_id)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </td>
      </template>
    </v-data-table>
    <ConfirmDeleteDialog
      :flagged-for-deletion="'spare part entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import { apiDeleteSparepartitemItem } from '../../components/api/SparepartitemApi';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';

export default {
  name: 'SparepartsTable',
  components: { ConfirmDeleteDialog },
  props: {
    sparepartItems: {
      type: Array,
      required: true,
    },
    sparepartsSearch: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    headers: [
      {
        text: 'Part',
        align: 'start',
        sortable: true,
        value: 'name',
      },
      {
        text: 'Stock',
        align: 'start',
        sortable: false,
        value: 'current_stock',
      },
      {
        text: 'Warn at',
        align: 'start',
        sortable: false,
        value: 'min_stock',
      },
    ],
    expanded: [],
    sparepartitem_id: null,
    confirm_delete_dialog: false,
  }),
  computed: {
    sparepart_items() {
      return this.sparepartItems;
    },
    spareparts_search: {
      get() {
        return this.sparepartsSearch;
      },
      set(value) {
        this.$emit('update:sparepartsSearch', value);
      },
    },
  },
  updated() {
    this.window_width = window.innerWidth;
  },
  created() {
    this.window_width = window.innerWidth;
  },
  methods: {
    expandRow(item) {
      this.expanded = item === this.expanded[0] ? [] : [item];
    },
    onEditButton(sparepartitemId) {
      this.$emit('editButtonClicked', sparepartitemId);
    },
    onDeleteButton(sparepartitemId) {
      this.sparepartitem_id = sparepartitemId;
      this.confirm_delete_dialog = true;
    },
    deletionConfirmed() {
      apiDeleteSparepartitemItem(this.sparepartitem_id)
        .then(() => {
          this.$emit('deletionConfirmed', this.sparepartitem_id);
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: 'Spare part entry deleted!',
          });
        })
        .catch((error) => {
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
  },
};
</script>

<style scoped>

</style>
