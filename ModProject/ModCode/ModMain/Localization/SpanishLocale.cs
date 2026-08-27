using System;
using System.Collections.Generic;
using System.Reflection;
using System.IO;
using Newtonsoft.Json.Linq;
using UnityEngine;

namespace MOD_pzAi9g.Localization
{
    internal static class SpanishLocale
    {
        private const string ResourcePrefix = "MOD_pzAi9g.Localization.Spanish.";
        private const string SelectionPreference = "TL-Spanish.Selected";

        private static readonly Dictionary<string, string> localTextByKey =
            new Dictionary<string, string>(StringComparer.Ordinal);
        private static readonly Dictionary<int, string> roleLogById =
            new Dictionary<int, string>();
        private static readonly Dictionary<int, string> npcNameFirstById =
            new Dictionary<int, string>();
        private static readonly Dictionary<int, string> herdNpcNameFirstById =
            new Dictionary<int, string>();
        private static readonly Dictionary<int, string> npcNameLastById =
            new Dictionary<int, string>();
        private static readonly Dictionary<int, string> prefixNameById =
            new Dictionary<int, string>();

        internal static bool Enabled { get; private set; } = true;
        internal static bool Selected { get; private set; }
        private static bool applyHerdNamesOnStartup;
        private static bool herdNamesApplied;

        internal static void Load()
        {
            Selected = PlayerPrefs.GetInt(SelectionPreference, 0) == 1;
            Enabled = Selected;
            applyHerdNamesOnStartup = Selected;
            herdNamesApplied = false;

            localTextByKey.Clear();
            roleLogById.Clear();
            npcNameFirstById.Clear();
            herdNpcNameFirstById.Clear();
            npcNameLastById.Clear();
            prefixNameById.Clear();

            LoadKeyedFile("LocalText.json", localTextByKey);
            LoadIdFile("RoleLogLocal.json", roleLogById);
            LoadIdFile("Npcs/HerdNPCNameFirst.json", herdNpcNameFirstById);
            LoadIdFile("Npcs/NpcNameFirst.json", npcNameFirstById);
            LoadIdFile("Npcs/NpcNameLast.json", npcNameLastById);
            LoadIdFile("Prefixes/BattleSkillPrefixName.json", prefixNameById);

            Debug.Log(
                "[TL-Spanish] Loaded locale data: " +
                localTextByKey.Count + " LocalText, " +
                roleLogById.Count + " RoleLogLocal, " +
                npcNameFirstById.Count + " first names, " +
                herdNpcNameFirstById.Count + " herd first names, " +
                npcNameLastById.Count + " last names, " +
                prefixNameById.Count + " prefixes.");
        }

        internal static void Toggle()
        {
            Enabled = !Enabled;
            Debug.Log("[TL-Spanish] Spanish locale " + (Enabled ? "enabled" : "disabled") + ".");
        }

        internal static void SetSelected(bool selected)
        {
            Selected = selected;
            Enabled = selected;
            PlayerPrefs.SetInt(SelectionPreference, selected ? 1 : 0);
            PlayerPrefs.Save();
        }

        internal static void ApplyHerdNpcNames()
        {
            if (!applyHerdNamesOnStartup || herdNamesApplied || g.conf == null)
                return;

            ConfHerdNPCNameFirst catalog = g.conf.herdNPCNameFirst;
            if (catalog == null || catalog._allConfList == null)
                return;

            int translated = 0;
            for (int index = 0; index < catalog._allConfList.Count; index++)
            {
                ConfHerdNPCNameFirstItem item = catalog._allConfList[index];
                string value;
                if (TryHerdNpcNameFirst(item, out value))
                {
                    item.name = value;
                    translated++;
                }
            }

            herdNamesApplied = true;
            Debug.Log("[TL-Spanish] Applied " + translated + " Herd NPC names.");
        }

        internal static string GetLanguageLabel()
        {
            string value;
            return localTextByKey.TryGetValue("ui_game_spanish", out value) && !string.IsNullOrEmpty(value)
                ? value
                : "Español";
        }

        internal static bool TryLocalText(ConfLocalTextItem item, out string value)
        {
            value = null;
            return Enabled && item != null && localTextByKey.TryGetValue(item.key, out value);
        }

        internal static bool TryLocalText(string key, out string value)
        {
            value = null;
            return Enabled && !string.IsNullOrEmpty(key) && localTextByKey.TryGetValue(key, out value);
        }

        internal static bool TryRoleLog(ConfRoleLogLocalItem item, out string value)
        {
            value = null;
            return Enabled && item != null && roleLogById.TryGetValue(item.id, out value);
        }

        internal static bool TryNpcNameFirst(ConfNpcNameFirstItem item, out string value)
        {
            value = null;
            return Enabled && item != null && npcNameFirstById.TryGetValue(item.id, out value);
        }

        internal static bool TryHerdNpcNameFirst(ConfHerdNPCNameFirstItem item, out string value)
        {
            value = null;
            return Enabled && item != null && herdNpcNameFirstById.TryGetValue(item.id, out value);
        }

        internal static bool TryNpcNameLast(ConfNpcNameLastItem item, out string value)
        {
            value = null;
            return Enabled && item != null && npcNameLastById.TryGetValue(item.id, out value);
        }

        internal static bool TryPrefixName(ConfBattleSkillPrefixNameItem item, out string value)
        {
            value = null;
            return Enabled && item != null && prefixNameById.TryGetValue(item.id, out value);
        }

        private static void LoadKeyedFile(string fileName, Dictionary<string, string> destination)
        {
            JArray entries = LoadArray(fileName);
            if (entries == null) return;

            foreach (JToken entry in entries)
            {
                string key = (string)entry["key"];
                string text = (string)entry["es"];
                if (!string.IsNullOrEmpty(key) && text != null)
                    destination[key] = text;
            }
        }

        private static void LoadIdFile(string fileName, Dictionary<int, string> destination)
        {
            JArray entries = LoadArray(fileName);
            if (entries == null) return;

            foreach (JToken entry in entries)
            {
                int id;
                string idText = (string)entry["id"];
                string text = (string)entry["es"];
                if (int.TryParse(idText, out id) && text != null)
                    destination[id] = text;
            }
        }

        private static JArray LoadArray(string fileName)
        {
            string resourceName = ResourcePrefix + fileName.Replace('/', '.');
            Assembly assembly = Assembly.GetExecutingAssembly();
            using (Stream stream = assembly.GetManifestResourceStream(resourceName))
            {
                if (stream == null)
                {
                    Debug.LogError("[TL-Spanish] Locale resource not found: " + resourceName);
                    return null;
                }

                try
                {
                    using (StreamReader reader = new StreamReader(stream))
                        return JArray.Parse(reader.ReadToEnd());
                }
                catch (Exception exception)
                {
                    Debug.LogError("[TL-Spanish] Could not read locale resource " + resourceName + ": " + exception);
                    return null;
                }
            }
        }
    }
}
