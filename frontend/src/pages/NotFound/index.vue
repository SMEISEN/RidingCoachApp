<template>
  <v-container fill-height fluid>
    <v-row
      align="center"
      justify="center"
    >
      <v-row justify="center" align="end">
        <v-col
          cols="11"
          xs="5"
          sm="5"
          md="5"
        >
          <v-row justify="end">
            <h1>
              404.
            </h1>
          </v-row>
          <v-row justify="end">
            <p class="text--secondary">
              That’s an error.
            </p>
          </v-row>
        </v-col>
        <v-col
          cols="11"
          xs="1"
          sm="1"
          md="1"
        />
        <v-col
          cols="11"
          xs="5"
          sm="5"
          md="5"
        >
          <v-row justify="start">
            <p>
              {{ `The requested URL ${$route.path} was not found on this server.` }}
            </p>
          </v-row>
          <v-row justify="start">
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
};
</script>

<style scoped>

</style>
