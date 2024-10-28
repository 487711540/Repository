<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import SidenavItem from "./SidenavItem.vue";


const store = useStore();
const isRTL = computed(() => store.state.isRTL);

const getRoute = () => {
  const route = useRoute();
  const routeArr = route.path.split("/");
  return routeArr[1];
};
</script>
<template>
  <div
    class="collapse navbar-collapse w-auto h-auto h-100"
    id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">


      <li class="nav-item">
        <sidenav-item
          to="/HomePage"
          :class="getRoute() === 'HomePage' ? 'active' : ''"
          :navText="'主页'"
        >
          <template v-slot:icon>
            <i class="ni ni-credit-card text-success text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

      <li class="nav-item">
        <sidenav-item
          to="/User"
          :class="getRoute() === 'User' ? 'active' : ''"
          :navText="'用户'"
        >
          <template v-slot:icon>
            <i class="ni ni-single-02 text-success text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

      <li class="nav-item">
        <sidenav-item
          to="/Collection"
          :class="getRoute() === 'Collection' ? 'active' : ''"
          :navText="'收藏'"
        >
        <template v-slot:icon>
            <i class="ni ni-favourite-28 text-success text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>



      <li class="nav-item">
        <sidenav-item
          to="/Settings"
          :class="getRoute() === 'Settings' ? 'active' : ''"
          :navText="'设置'"
        >
        <template v-slot:icon>
            <i class="ni ni-settings text-success text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
          :class="'ms-2'"
        >
          ACCOUNT PAGES
        </h6>
      </li>


      <li class="nav-item">
        <sidenav-item
          to="/signin"
          :class="getRoute() === 'signin' ? 'active' : ''"
          :navText="'登录'"
        >
          <template v-slot:icon>
            <i class="ni ni-single-copy-04 text-danger text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>

      <li class="nav-item">
        <sidenav-item
          to="/signup"
          :class="getRoute() === 'signup' ? 'active' : ''"
          :navText="isRTL ? '' : '注册'"
        >
          <template v-slot:icon>
            <i class="ni ni-collection text-info text-sm opacity-10"></i>
          </template>
        </sidenav-item>
      </li>
    </ul>
  </div>


</template>
