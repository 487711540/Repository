<script setup>
import ArgonInput from "@/components/ArgonInput.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import axios from "axios";
import { useStore } from "vuex";

const store = useStore();
const router = useRouter();

const username = ref(""); // 从 Vuex 中获取当前用户名
const password = ref("");

// 在组件挂载时获取当前用户名
username.value = store.state.username; // 从 Vuex 中获取当前用户名

const change = () => {
    const formData = new FormData();
    formData.append("username", username.value); // 使用 Vuex 中的用户名
    // formData.append("password", password.value);

    console.log("准备发送的数据：", {
        username: username.value,
        password: password.value,
    });

    axios.post("http://localhost:5000/change", formData,{
        withCredentials: true // 确保请求中带上 Cookie
    })
        .then((response) => {
            console.log(response.data);

            if (response.data.code === 200) {
                console.log("用户信息修改成功");
                console.log(response);
                
                alert("用户信息修改成功，请重新登录。");
                router.push("/signin"); // 修改成功后跳转到登录页面
            } else {
                console.error("修改用户信息失败:", response.data.msg);
                console.log(response);
                
                alert(`修改失败: ${response.data.msg}`); // 提示用户失败原因
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("修改过程中出现错误，请稍后再试。"); // 提示用户发生错误
            
            
        });
};




// const change = async () => {
//     const formData = new URLSearchParams();
//     formData.append("username", username.value); // 使用 Vuex 中的用户名
//     formData.append("password", password.value);

//     try {
//         // 发送 POST 请求到后端
//         const response = await axios.post("http://localhost:5000/change", formData, {
//             headers: {
//                 "Content-Type": "application/x-www-form-urlencoded",
//             },
//         });

//         // 检查请求是否成功
//         if (response.data.code === 200) {
//             console.log("用户信息修改成功");
//             console.log("Username:", username.value);
//             console.log("Password:", password.value);
//             console.log(response);
//            console.log(response.data);
           

            
//             router.push("/signin"); // 修改成功后跳转到登录页面
//         } else {
//             console.error("修改用户信息失败:", response.data.msg);
//         }
//     } catch (error) {
//         console.error("Error:", error);
//     }
// };
</script>

<template>
    <div class="container">
        <h1>修改用户信息</h1>

        <div class="input-container">
            <label for="username">账号</label>
            <argon-input v-model="username" id="username" type="text" placeholder="输入账号" name="username" size="lg"  />
        </div>

        <!-- 仅当用户名不是"游客"时显示密码输入框 -->
        <div class="input-container" v-if="username !== '游客'">
            <label for="password">密码</label>
            <argon-input v-model="password" id="password" type="password" placeholder="输入新密码" name="password" size="lg" />
        </div>

        <button class="submit-btn" @click="change" v-if="username !== '游客'">修改</button>
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
