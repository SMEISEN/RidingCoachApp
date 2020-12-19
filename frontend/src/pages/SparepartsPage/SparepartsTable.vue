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
      <template v-slot:item.current_stock="props">
        <SparepartsItemDialogForm
          :sparepart-item="props.item"
          :sparepart-child.sync="sparepart_child"
          :sparepart-child-template="sparepart_child_template"
          @initForm="initForm"
          @addSparepartItems="addSparepartItems"
        />
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
              required
              :rules="[v => (v) >= 0]"
              single-line
              prepend-icon="mdi-minus"
              append-outer-icon="mdi-plus"
              @click:prepend.prevent="
                props.item.min_stock = decreaseStock(props.item.min_stock)"
              @click:append-outer.prevent="
                props.item.min_stock = increaseStock(props.item.min_stock)"
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
            <td style="min-width: 115px; width: 6000px">
              <v-edit-dialog
                :return-value.sync="item.description"
                @save="changeSparepartItem(item.sparepartitem_id, item)"
              >
                {{ item.description }}
                <template v-slot:input>
                  <v-text-field
                    v-model="item.description"
                    single-line
                  />
                </template>
              </v-edit-dialog>
            </td>
            <td style="min-width: 95px; width: 4200px">
              <v-edit-dialog
                :return-value.sync="item.condition"
                @save="changeSparepartItem(item.sparepartitem_id, item)"
              >
                {{ item.condition }}
                <template v-slot:input>
                  <v-text-field
                    v-model="item.condition"
                    single-line
                  />
                </template>
              </v-edit-dialog>
            </td>
            <td style="min-width: 5px; width: 4550px">
              <v-edit-dialog
                :return-value.sync="item.stock"
                @save="changeSparepartItem(item.sparepartitem_id, item)"
              >
                {{ item.stock }}
                <template v-slot:input>
                  <v-text-field
                    v-model="item.stock"
                    single-line
                    :rules="[v => (v) >= 0]"
                    prepend-icon="mdi-minus"
                    append-outer-icon="mdi-plus"
                    @click:prepend.prevent="item.stock = decreaseStock(item.stock)"
                    @click:append-outer.prevent="item.stock = increaseStock(item.stock)"
                  />
                </template>
              </v-edit-dialog>
            </td>
            <td>
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
      :sparepart-parent.sync="sparepart_parent"
      :sparepart-child.sync="sparepart_child"
      :sparepart-child-template="sparepart_child_template"
      @initForm="initForm"
      @addSparepart="addSparepart"
    />
    <ConfirmDeleteDialog
      :flagged-for-deletion="'spare part entry'"
      :confirm-delete-dialog.sync="confirm_delete_dialog"
      @deleteConfirmationButtonClicked="deletionConfirmed()"
    />
  </div>
</template>

<script>
import {
  apiDeleteSparepartitemItem,
  apiPostSparepartitem,
  apiPutSparepartitemItem,
} from '../../components/api/SparepartitemApi';
import {
  apiPostSparepart,
  apiPutSparepartItem,
} from '../../components/api/SparepartApi';
import {
  incrementNumber,
  decrementNumber,
  initObject,
} from '../../components/utils/FromUtils';
import SparepartsDialogForm from './SparepartsDialogForm.vue';
import SparepartsItemDialogForm from './SparepartsItemDialogForm.vue';
import ConfirmDeleteDialog from '../../components/common/ConfirmDeleteDialog.vue';

export default {
  name: 'SparepartsTable',
  components: {
    ConfirmDeleteDialog,
    SparepartsItemDialogForm,
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
        text: 'Warn at',
        align: 'start',
        sortable: false,
        value: 'min_stock',
      },
      {
        text: 'Stock',
        align: 'start',
        sortable: false,
        value: 'current_stock',
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
    sparepart_parent: {
      name: null,
      module: null,
      min_stock: null,
    },
    sparepart_child: [],
    sparepart_child_template: {
      description: 'original',
      condition: 'new',
      stock: 1,
    },
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
    this.sparepart_child.push(this._.cloneDeep(this.sparepart_child_template));
  },
  methods: {
    onDeleteButton(sparepartitemId) {
      this.sparepartitem_id = sparepartitemId;
      this.confirm_delete_dialog = true;
    },
    deletionConfirmed() {
      apiDeleteSparepartitemItem(this.sparepartitem_id)
        .then(() => {
          this.$emit('refreshSpareParts');
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
          this.$emit('refreshSpareParts');
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
            message: 'Spare part edited!',
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
    changeSparepartItem(sparepartitemId, payload) {
      apiPutSparepartitemItem(payload, sparepartitemId)
        .then(() => {
          this.$emit('refreshSpareParts');
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'success',
            message: 'Spare part item edited!',
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
    addSparepart() {
      apiPostSparepart(this.sparepart_parent)
        .then((res) => {
          this.addSparepartItems(res.data);
          this.$emit('refreshSpareParts');
        })
        .catch((error) => {
          this.spareparts_dialog = false;
          this.$store.commit('setInfoSnackbar', {
            state: true,
            color: 'error',
            message: `${error}!`,
          });
        });
    },
    addSparepartItems(sparepartId) {
      const payload = this.sparepart_child.map((o) => ({ ...o, sparepart_id: sparepartId }));
      for (let i = 0; i < this.sparepart_child.length; i += 1) {
        apiPostSparepartitem(payload[i])
          .then(() => {
            if (i === this.sparepart_child.length - 1) {
              this.$emit('refreshSpareParts');
              this.spareparts_dialog = false;
              this.initForm();
              this.$store.commit('setInfoSnackbar', {
                state: true,
                color: 'success',
                message: 'Spare part(s) added!',
              });
            }
          })
          .catch((error) => {
            this.$emit('refreshSpareParts');
            this.spareparts_dialog = false;
            this.$store.commit('setInfoSnackbar', {
              state: true,
              color: 'error',
              message: `${error}!`,
            });
          });
      }
    },
    initForm() {
      initObject(this.sparepart_parent, null);
      this.sparepart_child = [this._.cloneDeep(this.sparepart_child_template)];
    },
  },
};
</script>

<style scoped>

</style>
