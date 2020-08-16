<template>
  <v-container
    fill-height
    fluid
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-row
        justify="center"
        align="end"
      >
        <v-col
          cols="12"
          xs="6"
          sm="6"
          md="6"
        >
          <v-row
            justify="end"
            dense
          >
            <h1>
              404.
            </h1>
          </v-row>
          <v-row
            justify="end"
            dense
          >
            <p class="text--secondary">
              That’s an error.
            </p>
          </v-row>
        </v-col>
        <v-col
          cols="12"
          xs="6"
          sm="6"
          md="6"
        >
          <v-row
            justify="start"
            dense
          >
            <p>
              {{ `The requested URL ${$route.path} was not found on this server.` }}
            </p>
          </v-row>
          <v-row
            justify="start"
            dense
          >
            <p class="text--secondary">
              {{ 'That’s all we know.' }}
            </p>
          </v-row>
        </v-col>
      </v-row>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound',
  metaInfo: {
    title: 'Page not found',
  },
};
</script>

<style scoped>

</style>
