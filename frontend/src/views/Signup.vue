<script setup>
import { onBeforeUnmount, onBeforeMount } from "vue";
import { useStore } from "vuex";
import ArgonInput from "@/components/ArgonInput.vue";
import ArgonButton from "@/components/ArgonButton.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { ref } from "vue";
import Mock from "mockjs";
import { mockUserDatabase } from "./mockUserDatabase";

// 模拟注册接口
Mock.mock("http://localhost:5000/register", "post", (options) => {
  const { username, password, confirmPassword } = JSON.parse(options.body);

  // 检查用户名是否已经注册
  const userExists = mockUserDatabase.some(user => user.username === username);

  if (userExists) {
    return {
      status: 401,
      message: "注册失败，用户名已存在",
    };
  }

  // 检查密码是否匹配
  if (password === confirmPassword) {
    // 注册成功，将用户存入模拟的数据库
    mockUserDatabase.push({ username, password });

    return {
      status: 200,
      message: "注册成功",
      token: "mock-token-789456",
    };
  } else {
    return {
      status: 401,
      message: "注册失败，密码和确认密码不匹配",
    };
  }
});

const store = useStore();
const router = useRouter();

// 绑定输入框的数据
const username = ref("");
const password = ref("");
const confirmPassword = ref("");

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

// 注册处理函数
const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert("密码和确认密码不匹配");
    return;
  }

  try {
    const response = await axios.post("http://localhost:5000/register", {
      username: username.value,
      password: password.value,
      confirmPassword: confirmPassword.value,
    });

    if (response.data.status === 200) {
      console.log("注册成功:", response.data);
      store.commit("setToken", response.data.token);
      router.push("/signin");
    } else {
      alert(response.data.message || "注册失败，请检查信息是否正确");
    }
  } catch (error) {
    console.error("注册失败:", error);
    alert("注册失败，请检查网络或服务器设置");
  }
};

// 返回跳转方法
const goBack = () => {
  router.push("/Signin");
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

          <!-- 注册标题和用户图标 -->
          <div class="row d-flex align-items-center justify-content-center mb-4">
            <div class="col-auto d-flex align-items-center">
              <i class="ni ni-circle-08 me-3" style="font-size: 30px;"></i>
              <h4 class="font-weight-bolder">注册</h4>
            </div>
          </div>

          <!-- 注册说明文字 -->
          <div class="row d-flex align-items-center justify-content-center mb-2">
            <div class="col-xl-4 col-lg-5 col-md-7">
              <p class="text-start">请输入账号和密码以完成注册</p>
            </div>
          </div>

          <!-- 账号输入部分 -->
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

          <!-- 密码输入部分 -->
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

          <!-- 确认密码输入部分 -->
          <div class="row d-flex align-items-center justify-content-center mb-3">
            <!-- 确认密码标签 -->
            <div class="col-auto">
              <label for="confirmPassword" class="form-label">确认密码</label>
            </div>

            <!-- 确认密码输入框 -->
            <div class="col-xl-4 col-lg-5 col-md-7">
              <argon-input id="confirmPassword" v-model="confirmPassword" type="password" name="confirmPassword"
                size="lg" class="w-100" />
            </div>
          </div>

          <!-- 注册按钮部分 -->
          <div class="row d-flex justify-content-center mt-4">
            <div class="col-xl-4 col-lg-5 col-md-7">
              <argon-button class="mt-4" variant="gradient" color="success" fullWidth size="lg" @click="handleRegister">
                注册
              </argon-button>
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
