import axios from 'axios';
import { API_HOST } from '../config.json';

export function sendMessage(sender, message) {
  return axios.post(`${API_HOST}/Answer/`, { sender, message });
}

export function QuuryActor(queryParams) {
  return axios.get(`${API_HOST}/QueryActor/`, { params: queryParams });
}
export function QueryMovie(queryParams) {
  return axios.get(`${API_HOST}/QueryMovie/`, { params: queryParams });
}
