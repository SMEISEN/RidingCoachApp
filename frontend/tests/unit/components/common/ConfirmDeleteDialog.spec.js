import ConfirmDeleteDialog from '@/components/common/ConfirmDeleteDialog';
import vuetify from '@/plugins/vuetify';
import Vuetify from 'vuetify';
import { addElemWithDataAppToBody } from '../../../utils';

import {
  mount,
  createLocalVue
} from '@vue/test-utils';

const localVue = createLocalVue();
localVue.use(Vuetify);

let wrapper;
const testItem = 'test item';

beforeEach(() => {
  addElemWithDataAppToBody();
  wrapper = mount(ConfirmDeleteDialog, {
    localVue,
    vuetify,
    propsData: {
      confirmDeleteDialog: true,
      flaggedForDeletion: testItem
    }
  });
});

afterEach(() => {
  wrapper.destroy();
});

describe('render the confirm delete dialog', () => {

  it('renders the dialog naming the item to be deleted',
    async () => {
      expect(wrapper.find('#confirmQuestion').text()).toEqual(expect.stringContaining(testItem));
  })

  it('emits the events of the cancel button',
    async () => {
      wrapper.vm.onCancel();
      expect(wrapper.emitted()['cancelButtonClicked']).toEqual([[]]);
      expect(wrapper.emitted()['update:confirmDeleteDialog']).toEqual([[false]]);
  })

  it('emits the events of the delete button',
    async () => {
      wrapper.vm.onConfirm();
      expect(wrapper.emitted()['deleteConfirmationButtonClicked']).toEqual([[]]);
      expect(wrapper.emitted()['update:confirmDeleteDialog']).toEqual([[false]]);
  })

  it('calls onCancel() when pressing the cancel button',
    async () => {
      const cancelButton = wrapper.find('#cancelButton');
      const spy = jest.spyOn(wrapper.vm, 'onCancel');
      cancelButton.trigger('click');

      await wrapper.vm.$nextTick();

      expect(spy).toHaveBeenCalled();
    })

  it('calls onConfirm() when pressing the cancel button',
    async () => {
      const confirmButton = wrapper.find('#confirmButton');
      const spy = jest.spyOn(wrapper.vm, 'onConfirm');
      confirmButton.trigger('click');

      await wrapper.vm.$nextTick();

      expect(spy).toHaveBeenCalled();
    })

});


