import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import Signup from "../views/Signup.vue";
import Signin from "../views/Signin.vue";
import User from "../views/User.vue";
import Settings from "../views/Settings.vue";
import Collection from "../views/Collection.vue";
import Personalization from "../views/Personalization.vue";

const routes = [
  {
    path: "/",
    name: "/",
    redirect: "/HomePage",
  },
  {
    path: "/HomePage",
    name: "回家",
    component: HomePage,
  },
  {
    path: "/User",
    name: "用户",
    component: User,
  },
  {
    path: "/Collection",
    name: "收藏",
    component: Collection,
  },
 {
    path: "/Personalization/:id",
    name: "个性化推荐",
    component: Personalization,
  },
  {
    path: "/Settings",
    name: "设置",
    component: Settings,
  },
  {
    path: "/signin",
    name: "Signin",
    component: Signin,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

export default router;
