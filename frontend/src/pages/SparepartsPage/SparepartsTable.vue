<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="sparepart_items"
      :search="spareparts_search"
      :expanded.sync="expanded"
      :footer-props="{ itemsPerPageText: '' }"
      item-key="sparepart_id"
      show-expand
      single-expand
    >
      <template v-slot:item.name="props">
        <v-edit-dialog
          :return-value.sync="props.item.name"
          @save="changeSparepartName(props.item.sparepart_id, props.item.name)"
        >
          {{ props.item.name }}
          <template v-slot:input>
            <v-text-field
              v-model="props.item.name"
              single-line
            />
          </template>
        </v-edit-dialog>
      </template>
      <template v-slot:item.min_stock="props">
        <v-edit-dialog
          :return-value.sync="props.item.min_stock"
          @save="changeSparepartMinStock(props.item.sparepart_id, props.item.min_stock)"
        >
          {{ props.item.min_stock }}
          <template v-slot:input>
            <v-text-field
              v-model.number="props.item.min_stock"
              style="max-width: 85px"
              single-line
              prepend-icon="mdi-minus"
              append-outer-icon="mdi-plus"
              @click:prepend="props.item.min_stock = decreaseStock(props.item.min_stock)"
              @click:append-outer="props.item.min_stock = increaseStock(props.item.min_stock)"
            />
          </template>
        </v-edit-dialog>
      </template>
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
    <v-card-text style="height: 5px; position: relative">
      <v-btn
        class="mt-n7"
        absolute
        x-small
        fab
        top
        left
        color="primary"
        @click.prevent="sparepart_dialog = true"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-card-text>
    <SparepartsDialogForm
      :bike-modules="bikeModules"
      :spareparts-dialog.sync="sparepart_dialog"
      @saveButtonClicked="$emit('refreshSpareParts')"
    />
    <ConfirmDeleteDialog
      :flagged-for-deletion="'spare part entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import { apiDeleteSparepartitemItem } from '../../components/api/SparepartitemApi';
import { apiPutSparepartItem } from '../../components/api/SparepartApi';
import {
  incrementNumber,
  decrementNumber,
} from '../../components/utils/FromUtils';
import SparepartsDialogForm from './SparepartsDialogForm.vue';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';

export default {
  name: 'SparepartsTable',
  components: {
    ConfirmDeleteDialog,
    SparepartsDialogForm,
  },
  props: {
    sparepartItems: {
      type: Array,
      required: true,
    },
    sparepartsSearch: {
      type: String,
      required: true,
    },
    bikeModules: {
      type: Array,
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
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    expanded: [],
    sparepartitem_id: null,
    sparepart_dialog: false,
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
            color: 'success',
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
    changeSparepartName(sparepartId, newName) {
      const payload = { name: newName };
      apiPutSparepartItem(payload, sparepartId)
        .then(() => {
          this.$emit('deletionConfirmed', this.sparepartitem_id);
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Spare part entry edited!',
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
    changeSparepartMinStock(sparepartId, newMinStock) {
      const payload = { min_stock: newMinStock };
      apiPutSparepartItem(payload, sparepartId)
        .then(() => {
          this.$emit('deletionConfirmed', this.sparepartitem_id);
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Spare part entry edited!',
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
    increaseStock(minStock) {
      return incrementNumber(minStock, 1);
    },
    decreaseStock(minStock) {
      return decrementNumber(minStock, 1);
    },
  },
};
</script>

<style scoped>

</style>
