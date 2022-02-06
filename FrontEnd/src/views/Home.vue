  <template>
  <el-card class="container">
    <div slot="header">
      <span class="title">Movie QA</span>
      <el-button
        type="text"
        @click="showTips = !showTips"
        style="float: right; padding: 5px 0;"
        >What can I do？</el-button
      >
    </div>
    <el-collapse-transition>
      <div class="tip-layer" v-show="showTips">
        <el-tabs tab-position="bottom" style="margin-bottom: 4px;">
          <el-tab-pane v-for="(tip, idx) in tips" :key="idx" :label="tip.title">
            <p class="tip-title">{{ tip.title }}</p>
            <span>{{ tip.desc }}</span>
            <el-button
              class="btn-try"
              type="primary"
              size="small"
              @click="sendMessage(getMsg(tip.message))"
              :loading="pending"
              >Try Now!</el-button
            >
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-collapse-transition>
    <div class="messages" v-chat-scroll="{ always: true, smooth: true }">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chatbox"
        :class="'user' + message.user"
      >
        {{ message.content }}
      </div>
    </div>
    <el-input
      v-model="input"
      placeholder="The first letter of the actor and the movie need to be capitalized, e.g. Titanic, Leonardo DiCaprio"
      @keyup.enter.native="!pending && sendMessage(input)"
    >
      <template slot="append">
        <el-button @click="sendMessage(input)" :loading="pending"
          >Send</el-button
        >
      </template>
    </el-input>
  </el-card>
</template>

<script>
import { sendMessage } from '@/api';

export default {
  name: 'home',
  data() {
    return {
      messages: [{ user: 1, content: 'Hello，I\'m your Movie assistant~' }],
      input: '',
      senderId:
        new Date().toISOString()
        + Math.random()
          .toString(36)
          .substr(2)
          .toUpperCase(),
      showTips: false,
      pending: false,
      tips: [
        {
          title: 'Film Field Knowledge Q&A',
          desc: 'Knowledge graph and semantic information based Q&A about the movie and the actor, to be more precise, the initials of the actor and the movie need to be capitalized, e.g. Titanic, Leonardo DiCaprio',
          message: ['When did Leonardo DiCaprio birth?', 'Where did Leonardo DiCaprio birth?', 'When didi Titanic release', 'What movies did Leonardo DiCaprio act in?', 'What actors appeared in Titanic?'],
        },
        {
          title: 'Advance Query',
          desc: 'Take advantage of the knowledge graph to perform advanced queries based on the relationships between actors and actors, movies and movies, and movies and actors.',
          message: ['Which movies did Leonardo DiCaprio and Andie Hicks star in together?', 'What are the movies Leonardo DiCaprio has starred in with a rating above 5?', 'How many movies has Harrison Ford starred in?'],
        },
      ],
    };
  },
  components: {},
  methods: {
    sendMessage(msg) {
      if (!msg) {
        return;
      }
      this.pending = true;
      this.messages.push({
        user: 0,
        content: msg,
      });
      sendMessage(this.senderId, msg)
        .then((res) => {
          console.log(res.data);
          this.messages.push({
            user: 1,
            content: res.data.answer,
          });

          this.pending = false;
        })
        .catch(() => {
          this.pending = false;
        });
      this.input = '';
    },
    getMsg(msg) {
      if (Array.isArray(msg)) {
        return msg[Math.floor(Math.random() * msg.length)];
      }
      return msg;
    },
  },
};
</script>

<style lang="scss" scoped>
.messages {
  overflow: scroll;
  margin-bottom: 20px;
  flex: 1;
  .chatbox {
    &.user0 {
      float: right;
      color: #000000;
      background-color: #94eb68;
    }
    &.user1 {
      float: left;
      color: #000000;
      background-color: #ededed;
    }
    padding: 5px 15px 6px;
    max-width: 300px;
    border-radius: 4px;
    clear: both;
    font-size: 13px;
    margin: 2px 0;
  }
}

.tip-layer {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
  background-color: #ededed;
  backdrop-filter: blur(5px);
  .tip-title {
    font-weight: bold;
  }
  .btn-try {
    position: absolute;
    top: 10px;
    right: 0;
  }
}
</style>
