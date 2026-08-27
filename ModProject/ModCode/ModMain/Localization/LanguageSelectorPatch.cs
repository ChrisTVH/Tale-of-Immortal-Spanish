using System;
using HarmonyLib;
using UnhollowerRuntimeLib;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace MOD_pzAi9g.Localization
{
    internal static class LanguageSelectorPatchState
    {
        private const string SpanishItemName = "TL-Spanish.LanguageItem";
        private const string LanguageRestartMessageKey = "ui_game_qiehuanyuyan2";

        private static UIGameSetting currentSettings;
        private static GameObject spanishItem;
        private static bool configured;

        internal static void ConfigureActiveSettings()
        {
            if (configured) return;

            UIGameSetting settings = UnityEngine.Object.FindObjectOfType<UIGameSetting>();
            if (settings == null) return;

            Configure(settings);
        }

        internal static void Reset()
        {
            currentSettings = null;
            spanishItem = null;
            configured = false;
        }

        private static void Configure(UIGameSetting settings)
        {
            if (settings.goLanguageItem == null || settings.goLanguageRoot == null)
            {
                Debug.LogWarning("[TL-Spanish] Language item template or root was unavailable.");
                return;
            }

            currentSettings = settings;
            AddNativeLanguageListeners(settings.goLanguageRoot.transform);
            spanishItem = CreateSpanishItem(settings);
            configured = spanishItem != null;

            if (configured)
            {
                RestoreSpanishSelection();
                Debug.Log("[TL-Spanish] Added standalone Spanish language item.");
            }
        }

        private static GameObject CreateSpanishItem(UIGameSetting settings)
        {
            GameObject item = UnityEngine.Object.Instantiate(
                settings.goLanguageItem,
                settings.goLanguageRoot.transform);
            item.name = SpanishItemName;
            item.SetActive(true);

            foreach (Text text in item.GetComponentsInChildren<Text>(true))
                text.text = "Español (Beta)";

            Button button = item.GetComponentInChildren<Button>(true);
            if (button == null)
            {
                Debug.LogError("[TL-Spanish] Spanish language item has no Button component.");
                UnityEngine.Object.Destroy(item);
                return null;
            }

            button.onClick.RemoveAllListeners();
            button.onClick.AddListener(CreateUnityAction(SelectSpanish));
            return item;
        }

        private static void AddNativeLanguageListeners(Transform root)
        {
            for (int index = 0; index < root.childCount; index++)
            {
                Button button = root.GetChild(index).GetComponentInChildren<Button>(true);
                if (button != null)
                    button.onClick.AddListener(CreateUnityAction(SelectNativeLanguage));
            }
        }

        private static void SelectSpanish()
        {
            SpanishLocale.SetSelected(true);
            RestoreSpanishSelection();
            CloseLanguageMenu();
            UITipItem.AddTip(GameTool.LS(LanguageRestartMessageKey), 3f);
            Debug.Log("[TL-Spanish] Spanish selected from the standalone language item.");
        }

        private static void SelectNativeLanguage()
        {
            SpanishLocale.SetSelected(false);
            Debug.Log("[TL-Spanish] Native language selected; Spanish disabled.");
        }

        private static void RestoreSpanishSelection()
        {
            if (!SpanishLocale.Selected || currentSettings == null) return;

            if (currentSettings.textLanguage != null)
                currentSettings.textLanguage.text = SpanishLocale.GetLanguageLabel();
        }

        private static void CloseLanguageMenu()
        {
            if (currentSettings == null) return;

            if (currentSettings.goLanguageMask != null)
                currentSettings.goLanguageMask.SetActive(false);
            if (currentSettings.tglLanguage != null)
                currentSettings.tglLanguage.SetIsOnWithoutNotify(false);
        }

        private static UnityAction CreateUnityAction(Action action)
        {
            return DelegateSupport.ConvertDelegate<UnityAction>(action);
        }
    }

    [HarmonyPatch(typeof(UIGameSetting), "Init")]
    internal static class LanguageSelectorInitPatch
    {
        private static void Postfix()
        {
            LanguageSelectorPatchState.ConfigureActiveSettings();
        }
    }

    [HarmonyPatch(typeof(UIGameSetting), "UpdateUI")]
    internal static class LanguageSelectorUpdatePatch
    {
        private static void Postfix()
        {
            LanguageSelectorPatchState.ConfigureActiveSettings();
        }
    }

    [HarmonyPatch(typeof(UIGameSetting), "Destroy")]
    internal static class LanguageSelectorDestroyPatch
    {
        private static void Postfix()
        {
            LanguageSelectorPatchState.Reset();
        }
    }
}
