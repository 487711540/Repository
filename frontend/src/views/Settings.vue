<script setup>
import { useStore } from "vuex";
import { activateDarkMode, deactivateDarkMode } from "@/assets/js/dark-mode";
import { useRouter } from "vue-router";
import Mock from "mockjs"; // 引入 Mock.js
import axios from "axios"; // 引入 axios 用于发送请求

const store = useStore();
const router = useRouter();

// 使用 Mock.js 模拟退出登录接口
Mock.mock("http://localhost:5000/logout", "post", {
    status: 200,
    message: "退出登录成功",
});

// Mutations for Sidebar
const setSidebarType = (type) => store.commit("sidebarType", type);

// Update sidebar color from dropdown
const updateSidebarColor = (event) => {
    const color = event.target.value;
    document.querySelector("#sidenav-main").setAttribute("data-color", color);
};

// Update sidebar type from dropdown
const updateSidebarType = (event) => {
    const type = event.target.value;
    setSidebarType(type);
};

// Update theme mode from dropdown
const updateThemeMode = (event) => {
    const mode = event.target.value;
    store.commit("darkMode", mode === "dark");
    if (mode === "dark") {
        store.state.darkMode = true;
        setSidebarType("bg-default");
        activateDarkMode();
    } else {
        store.state.darkMode = false;
        setSidebarType("bg-white");
        deactivateDarkMode();
    }
};

// Switch account from dropdown
const switchAccount = (event) => {
    const account = event.target.value;
    console.log(`Switching to ${account}`);
    // 可以在这里加入切换账号的逻辑
};

// Logout and navigate to the logout page
const logout = async () => {
    try {
        const response = await axios.post("http://localhost:5000/logout");

        if (response.status === 200) {
            console.log("退出登录成功");
            // 清除前端用户数据，可以清空 Vuex 的用户信息
            store.commit("setUser", null);
            router.push("/Signin"); // 重定向到登录页面
        } else {
            console.error("退出登录失败:", response.data.message);
        }
    } catch (error) {
        console.error("退出登录时出错:", error);
    }
};

// Complete and navigate to the home page
const complete = () => {
    console.log("Complete configuration...");
    router.push("/Billing");
};
</script>

<template>
    <div class="configurator-container">
        <hr class="my-1 horizontal dark" />

        <!-- Sidebar Backgrounds -->
        <div class="configurator-block">
            <div class="d-flex align-items-center mb-3 justify-content-center">
                <h6 class="mb-0 me-2">侧边框颜色</h6>
                <select class="form-select" @change="updateSidebarColor($event)">
                    <option disabled selected value>请选择</option>
                    <option value="primary">Primary</option>
                    <option value="dark">Dark</option>
                    <option value="info">Info</option>
                    <option value="success">Success</option>
                    <option value="warning">Warning</option>
                    <option value="danger">Danger</option>
                </select>
            </div>

            <!-- Sidenav Type -->
            <div class="d-flex align-items-center justify-content-center">
                <h6 class="mb-0 me-2">侧边栏类型</h6>
                <select class="form-select" @change="updateSidebarType($event)">
                    <option disabled selected value>请选择</option>
                    <option value="bg-white">白色</option>
                    <option value="bg-default">黑色</option>
                </select>
            </div>

            <!-- Theme Mode (Light/Dark) -->
            <div class="d-flex align-items-center justify-content-center mt-3">
                <h6 class="mb-0 me-2">主题模式</h6>
                <select class="form-select" @change="updateThemeMode($event)">
                    <option disabled selected value>请选择</option>
                    <option value="light">白天</option>
                    <option value="dark">夜间</option>
                </select>
            </div>

            <!-- Account Switch -->
            <div class="d-flex align-items-center justify-content-center mt-3">
                <h6 class="mb-0 me-2">切换账号</h6>
                <select class="form-select" @change="switchAccount($event)">
                    <option disabled selected value>请选择</option>
                    <option value="account1">账号1</option>
                    <option value="account2">账号2</option>
                    <option value="account3">账号3</option>
                </select>
            </div>

            <!-- Buttons -->
            <div class="button-group mt-4">
                <button class="btn btn-danger w-100 mb-2" @click="logout">退出登录</button>
                <button class="btn btn-success w-100" @click="complete">完成</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dark-theme {
    background-color: #121212;
    color: #ffffff;
}

.configurator-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
}

.configurator-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.form-select {
    width: 250px;
    padding: 10px;
    margin-bottom: 20px;
}

h6 {
    margin-bottom: 0.5rem;
    text-align: center;
}

.d-flex {
    justify-content: center;
    width: 100%;
}

.me-2 {
    width: 120px;
    text-align: right;
}

hr.horizontal {
    width: 100%;
    margin-top: 10px;
    margin-bottom: 20px;
}

.button-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 250px;
}
</style>
