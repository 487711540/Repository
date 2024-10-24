<script setup>
import { onBeforeUnmount, onBeforeMount } from "vue";
import { useStore } from "vuex";
import ArgonInput from "@/components/ArgonInput.vue";
import ArgonSwitch from "@/components/ArgonSwitch.vue";
import ArgonButton from "@/components/ArgonButton.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { ref } from "vue";
import Mock from "mockjs";
import { mockUserDatabase } from "./mockUserDatabase";

// 模拟登录接口，检查用户数据库中的信息
Mock.mock("http://localhost:5000/login", "post", (options) => {
  const { username, password } = JSON.parse(options.body);

  // 检查用户名和密码是否匹配
  const user = mockUserDatabase.find(user => user.username === username && user.password === password);

  if (user) {
    return {
      status: 200,
      message: "登录成功",
      token: "mock-token-123456",
    };
  } else {
    return {
      status: 401,
      message: "登录失败，账号或密码错误",
    };
  }
});

const store = useStore();
const router = useRouter();

// 绑定输入框的数据
const username = ref("");
const password = ref("");

// 组件挂载前的处理
onBeforeMount(() => {
  store.state.hideConfigButton = true;
  store.state.showNavbar = false;
  store.state.showSidenav = false;
  store.state.showFooter = false;
});

onBeforeUnmount(() => {
  store.state.hideConfigButton = false;
  store.state.showNavbar = true;
  store.state.showSidenav = true;
  store.state.showFooter = true;
});

// 登录处理函数
const handleLogin = async () => {
  try {
    const response = await axios.post("http://localhost:5000/login", {
      username: username.value,
      password: password.value,
    });

    if (response.data.status === 200) {
      console.log("登录成功:", response.data);
      store.commit("setToken", response.data.token);
      router.push("/homepage");
    } else {
      alert(response.data.message || "登录失败，请检查账号和密码");
    }
  } catch (error) {
    console.error("登录失败:", error);
    alert("登录失败，请检查网络或服务器设置");
  }
};

// 注册跳转方法
const goToSignup = () => {
  router.push("/signup");
};

const goBack = () => {
  router.push("/HomePage");
};
</script>


<template>
  <div class="container top-0 position-sticky z-index-sticky">
    <div class="row">
      <div class="col-12">
        <navbar isBlur="blur border-radius-lg my-3 py-2 start-0 end-0 mx-4 shadow" v-bind:darkMode="true"
          isBtn="bg-gradient-success" />
      </div>
    </div>
  </div>
  <main class="mt-0 main-content">
    <section>
      <div class="page-header min-vh-100 d-flex align-items-center justify-content-center">
        <div class="container position-relative">
          <button class="btn btn-secondary position-fixed top-3 start-3" @click="goBack">
            <i class="ni ni-bold-left"></i> 返回
          </button>

          <!-- 登录标题和用户图标 -->
          <div class="row d-flex align-items-center justify-content-center mb-4">
            <div class="col-auto d-flex align-items-center">
              <i class="ni ni-circle-08 me-3" style="font-size: 30px;"></i>
              <h4 class="font-weight-bolder">登录</h4>
            </div>
          </div>

          <!-- 登录说明文字 -->
          <div class="row d-flex align-items-center justify-content-center mb-2">
            <div class="col-xl-4 col-lg-5 col-md-7">
              <p class="text-start">输入您的账号和密码以登录</p>
            </div>
          </div>

          <!-- 账号、密码部分 -->
          <div class="row d-flex align-items-center justify-content-center mb-3">
            <!-- 账号标签 -->
            <div class="col-auto">
              <label for="username" class="form-label">账号</label>
            </div>

            <!-- 账号输入框 -->
            <div class="col-xl-4 col-lg-5 col-md-7">
              <argon-input id="username" v-model="username" type="text" name="username" size="lg" class="w-100" />
            </div>
          </div>

          <!-- 密码部分 -->
          <div class="row d-flex align-items-center justify-content-center mb-3">
            <!-- 密码标签 -->
            <div class="col-auto">
              <label for="password" class="form-label">密码</label>
            </div>

            <!-- 密码输入框 -->
            <div class="col-xl-4 col-lg-5 col-md-7">
              <argon-input id="password" v-model="password" type="password" name="password" size="lg" class="w-100" />
            </div>
          </div>

          <!-- 登录按钮部分 -->
          <div class="row d-flex justify-content-center mt-4">
            <div class="col-xl-4 col-lg-5 col-md-7">
              <argon-switch id="rememberMe" name="remember-me">记住我</argon-switch>
              <argon-button class="mt-4" variant="gradient" color="success" fullWidth size="lg" @click="handleLogin">
                登录
              </argon-button>
            </div>
          </div>

          <!-- 注册部分 -->
          <div class="row d-flex justify-content-center mt-3">
            <div class="col-xl-4 col-lg-5 col-md-7 text-center">
              <p class="mx-auto mb-4 text-sm">
                新用户请
                <a href="javascript:;" class="text-success text-gradient font-weight-bold" @click="goToSignup">注册</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.form-label {
  width: auto;
  text-align: left;
  margin-bottom: 0;
}

.argon-input {
  width: 100%;
}

.argon-button {
  width: 100%;
}

.col-xl-4,
.col-lg-5,
.col-md-7 {
  max-width: 100%;
}

.d-flex.align-items-center label {
  margin-bottom: 0;
}

.me-3 {
  margin-right: 16px;
}

.text-start {
  text-align: left;
}
</style>
