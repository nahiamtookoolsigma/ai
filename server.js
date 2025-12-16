import express from 'express';
import webpush from 'web-push';
import cors from 'cors';
const app = express();
app.use(cors());
app.use(express.json());

const subs = new Set(); // in-mem for demo; swap for DB in real life

webpush.setVapidDetails(
  'mailto:you@example.com',
  process.env.VAPID_PUBLIC,
  process.env.VAPID_PRIVATE
);

app.post('/save-sub', (req,res) => {
  subs.add(JSON.stringify(req.body));
  res.sendStatus(201);
});

app.get('/ping', (req,res) => { // manual trigger
  const payload = JSON.stringify({title:'Hi from Render', body:'works 🎉'});
  subs.forEach(s => webpush.sendNotification(JSON.parse(s), payload));
  res.send('pushed');
});

app.listen(process.env.PORT || 443);
