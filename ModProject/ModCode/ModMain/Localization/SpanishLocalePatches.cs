using HarmonyLib;

namespace MOD_pzAi9g.Localization
{
    internal static class SpanishLocaleTextFormatter
    {
        private const int DefaultBackgroundType = 1;

        internal static string Format(string value)
        {
            return Format(value, DefaultBackgroundType);
        }

        internal static string Format(string value, int backgroundType)
        {
            return GameTool.TextToData(value, backgroundType);
        }
    }

    [HarmonyPatch(typeof(GameTool), "LS", new[] { typeof(string) })]
    internal static class GameToolLsPatch
    {
        private static void Postfix(string keys, ref string __result)
        {
            string value;
            if (SpanishLocale.TryLocalText(keys, out value))
                __result = SpanishLocaleTextFormatter.Format(value);
            else if (keys == "ui_game_yingwen")
                __result = "English";
        }
    }

    [HarmonyPatch(typeof(GameTool), "LS", new[] { typeof(string), typeof(int) })]
    internal static class GameToolLsWithBackgroundPatch
    {
        private static void Postfix(string keys, int bgType, ref string __result)
        {
            string value;
            if (SpanishLocale.TryLocalText(keys, out value))
                __result = SpanishLocaleTextFormatter.Format(value, bgType);
            else if (keys == "ui_game_yingwen")
                __result = "English";
        }
    }

    [HarmonyPatch(typeof(ConfLocalTextEx), "text")]
    internal static class LocalTextPatch
    {
        private static void Postfix(ConfLocalTextItem item, ref string __result)
        {
            string value;
            if (SpanishLocale.TryLocalText(item, out value))
                __result = SpanishLocaleTextFormatter.Format(value);
            else if (item != null && item.key == "ui_game_yingwen")
                __result = "English";
        }
    }

    [HarmonyPatch(typeof(ConfRoleLogLocalEx), "text")]
    internal static class RoleLogLocalPatch
    {
        private static void Postfix(ConfRoleLogLocalItem item, ref string __result)
        {
            string value;
            if (SpanishLocale.TryRoleLog(item, out value))
                __result = SpanishLocaleTextFormatter.Format(value);
        }
    }

    [HarmonyPatch(typeof(ConfNpcNameFirstEx), "name")]
    internal static class NpcNameFirstPatch
    {
        private static void Postfix(ConfNpcNameFirstItem item, ref string __result)
        {
            string value;
            if (SpanishLocale.TryNpcNameFirst(item, out value))
                __result = value;
        }
    }

    [HarmonyPatch(typeof(ConfNpcNameLastEx), "name")]
    internal static class NpcNameLastPatch
    {
        private static void Postfix(ConfNpcNameLastItem item, ref string __result)
        {
            string value;
            if (SpanishLocale.TryNpcNameLast(item, out value))
                __result = value;
        }
    }

    [HarmonyPatch(typeof(ConfBattleSkillPrefixNameEx), "text")]
    internal static class BattleSkillPrefixNamePatch
    {
        private static void Postfix(ConfBattleSkillPrefixNameItem item, ref string __result)
        {
            string value;
            if (SpanishLocale.TryPrefixName(item, out value))
                __result = value;
        }
    }
}
