<script setup>
import { useStore } from "vuex";
import { activateDarkMode, deactivateDarkMode } from "@/assets/js/dark-mode";
import { useRouter } from "vue-router";
import axios from "axios"; // 引入 axios 用于发送请求

const store = useStore();
const router = useRouter();

// 设置侧边栏类型的 Mutation
const setSidebarType = (type) => store.commit("sidebarType", type);

// 更新侧边栏颜色
const updateSidebarColor = (event) => {
    const color = event.target.value;
    document.querySelector("#sidenav-main").setAttribute("data-color", color);
};

// 更新侧边栏类型
const updateSidebarType = (event) => {
    const type = event.target.value;
    setSidebarType(type);
};

// 更新主题模式
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

// 注销
const logout = async () => {
    try {
        const response = await axios.get("http://localhost:5000/logout");
        if (response.data.code === 200) {
            console.log("注销成功");
            store.commit("setUsername", "游客"); // 设置为游客状态
            router.push("/HomePage"); // 重定向到登录页面
        } else {
            console.error("注销失败:", response.data.msg);
        }
    } catch (error) {
        console.error("注销时出错:", error);
    }
};

</script>

<template>
    <div class="configurator-container">
        <hr class="my-1 horizontal dark" />

        <!-- 侧边栏背景 -->
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

            <!-- 侧边栏类型 -->
            <div class="d-flex align-items-center justify-content-center">
                <h6 class="mb-0 me-2">侧边栏类型</h6>
                <select class="form-select" @change="updateSidebarType($event)">
                    <option disabled selected value>请选择</option>
                    <option value="bg-white">白色</option>
                    <option value="bg-default">黑色</option>
                </select>
            </div>

            <!-- 主题模式 (白天/夜间) -->
            <div class="d-flex align-items-center justify-content-center mt-3">
                <h6 class="mb-0 me-2">主题模式</h6>
                <select class="form-select" @change="updateThemeMode($event)">
                    <option disabled selected value>请选择</option>
                    <option value="light">白天</option>
                    <option value="dark">夜间</option>
                </select>
            </div>

            <!-- 切换账号 -->
            <div class="d-flex align-items-center justify-content-center mt-3">
                <h6 class="mb-0 me-2">切换账号</h6>
                <select class="form-select" @change="switchAccount($event)">
                    <option disabled selected value>请选择</option>
                    <option value="account1">账号1</option>
                    <option value="account2">账号2</option>
                    <option value="account3">账号3</option>
                </select>
            </div>

            <!-- 按钮组 -->
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
