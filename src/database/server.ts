import { JsonDB, Config } from "node-json-db";
import { ServerSettings } from "../interfaces";

const db = new JsonDB(new Config("JSONDB/server", true, false, "/"));

export async function settings(id: string, options: ServerSettings) {
	if (!await db.exists(`/${id}`)) {
		return db.push(`/${id}`, options);
	}
	return db.push(`/${id}`, options);
}

export async function settingsExist(id: string) {
	return await db.exists(`/${id}`);
}

export async function getSettings(id: string,) {
	return await db.getData(`/${id}`);
}