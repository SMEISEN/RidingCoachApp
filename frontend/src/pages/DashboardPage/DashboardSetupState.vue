<template>
  <RadarChart
    :chart-data="data_collection"
    :options="data_options"
    :height="null"
    :width="null"
  />
</template>

<script>
import RadarChart from '../../components/common/RadarChart.vue';

export default {
  name: 'DashboardSetupState',
  components: {
    RadarChart,
  },
  props: {
    setupArray: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    data_collection: {
      labels: [],
      datasets: [],
    },
    data_sets: [
      {
        label: 'Current',
        data: [],
        backgroundColor: 'rgba(255,99,132,0.2)',
        borderColor: 'rgba(255,99,132,1)',
        pointBackgroundColor: 'rgba(255,99,132,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(255,99,132,1)',
      },
      {
        label: 'Standard',
        data: [],
        backgroundColor: 'rgba(179,181,198,0.2)',
        borderColor: 'rgba(179,181,198,1)',
        pointBackgroundColor: 'rgba(179,181,198,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(179,181,198,1)',
      },
    ],
    data_options: {
      responsive: true,
      maintainAspectRatio: true,
      title: {
        display: false,
        text: 'Suspension Data',
      },
      scale: {
        angleLines: {
          display: true,
        },
        ticks: {
          suggestedMin: -15,
          suggestedMax: 15,
          stepSize: 1,
        },
      },
      legend: {
        position: 'bottom',
        align: 'end',
        labels: {
          usePointStyle: true,
          fontSize: 10,
        },
      },
    },
  }),
  watch: {
    setupArray() {
      this.processSetupData();
    },
  },
  created() {
    this.processSetupData();
  },
  methods: {
    /**
     * Processes the setup data for the radar chart.
     */
    processSetupData() {
      this.data_sets[1].data = this.setupArray
        .map(() => 0);
      this.data_sets[0].data = this.setupArray
        .map((value) => value.ticks_current - value.ticks_standard);
      this.data_collection.datasets = this.data_sets;
      this.data_collection.labels = this.setupArray.map((value) => `${value.group} ${value.name}`);
      const allTicks = this.data_sets[1].data.concat(this.data_sets[0].data);
      this.data_options.scale.ticks.suggestedMin = Math.min(...allTicks) - 1;
      this.data_options.scale.ticks.suggestedMax = Math.max(...allTicks) + 1;
    },
  },
};
</script>
