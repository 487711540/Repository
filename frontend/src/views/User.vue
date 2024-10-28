<script setup>
import ArgonInput from "@/components/ArgonInput.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import axios from "axios"; // 导入 axios
import Mock from "mockjs";
import { mockUserDatabase } from "./mockUserDatabase";

// 模拟修改用户信息接口
Mock.mock("http://localhost:5000/change", "post", (options) => {
    const { nickname, username, password } = JSON.parse(options.body);
    const user = mockUserDatabase.find(user => user.username === username);

    if (user) {
        user.nickname = nickname;
        user.password = password;
        return {
            status: 200,
            message: "用户信息修改成功",
        };
    } else {
        return {
            status: 404,
            message: "用户不存在",
        };
    }
});

const router = useRouter();

const username = ref("");
const password = ref("");

// 修改提交函数
const change = async () => {
    const payload = {
        username: username.value,
        password: password.value,
    };

    try {
        // 发送POST请求到后端
        const response = await axios.post("http://localhost:5000/change", payload);

        // 检查请求是否成功
        if (response.status === 200) {
            console.log("用户信息修改成功");
            router.push("/signin");
        } else {
            console.error("修改用户信息失败:", response.data.message);
        }
    } catch (error) {
        console.error("Error:", error);
    }
};
</script>

<template>
    <div class="container">
        <h1>修改用户信息</h1>



        <div class="input-container">
            <label for="username">账号</label>
            <argon-input v-model="username" id="username" type="text" placeholder="输入账号" name="username" size="lg" />
        </div>

        <div class="input-container">
            <label for="password">密码</label>
            <argon-input v-model="password" id="password" type="password" placeholder="输入新密码" name="password"
                size="lg" />
        </div>

        <button class="submit-btn" @click="change">修改</button>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.input-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

label {
    width: 60px;
    margin-right: 10px;
    text-align: right;
    font-size: large;
}

h1 {
    margin-bottom: 20px;
}

.submit-btn {
    width: 100px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.submit-btn:hover {
    background-color: #0056b3;
}
</style>
