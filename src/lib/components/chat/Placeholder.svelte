<script lang="ts">
	import { getContext, createEventDispatcher, tick } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	import {
		config,
		user,
		models as _models,
		temporaryChatEnabled,
		selectedFolder,
		chats,
		currentChatPage
	} from '$lib/stores';
	import { WEBUI_API_BASE_URL } from '$lib/constants';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import EyeSlash from '$lib/components/icons/EyeSlash.svelte';

	const i18n = getContext('i18n');

	export let history;
	export let selectedModels: [''];
	export let prompt = '';
	export let files = [];
	export let autoScroll = false;
	export let selectedToolIds = [];
	export let selectedFilterIds = [];
	export let pendingOAuthTools = [];
	export let showCommands = false;
	export let imageGenerationEnabled = false;
	export let codeInterpreterEnabled = false;
	export let webSearchEnabled = false;
	export let atSelectedModel: Model | undefined;
	export let dragged = false;
	export let toolServers = [];
	export let stopResponse: Function;
	export let createMessagePair: Function;
	export let onUpload: Function = (e) => {};
	export let onSelect = (e) => {};

	let activeTab = 'models'; // 'models' | 'agents'
	let selectedModelIdx = 0;
	let models = [];

	$: if (selectedModels.length > 0) {
		selectedModelIdx = models.length - 1;
	}

	$: models = selectedModels.map((id) => $_models.find((m) => m.id === id));

	const modelCards = [
		{
			id: 'featured',
			title: '推荐模型',
			description: '与我们推荐的通用旗舰模型进行对话与创作。',
			prompt: '推荐一些你们最强大的模型',
			color: 'text-rose-500 bg-rose-50 dark:bg-rose-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/></svg>`
		},
		{
			id: 'code',
			title: '代码与对话',
			description: '编写、调试代码，或进行深度的技术问题讨论。',
			prompt: '帮我写一个快速排序算法的 Python 实现',
			color: 'text-blue-500 bg-blue-50 dark:bg-blue-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>`
		},
		{
			id: 'image',
			title: '图像生成',
			description: '输入文字描述，自动绘制精美图像和视觉设计。',
			prompt: '画一只在林中漫步的机械梅花鹿，赛博朋克风格',
			color: 'text-amber-500 bg-amber-50 dark:bg-amber-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>`
		},
		{
			id: 'video',
			title: '视频生成',
			description: '通过提示词生成流畅、富有创意的短视频与动图。',
			prompt: '生成一段未来科幻城市穿梭的 3 秒短视频',
			color: 'text-purple-500 bg-purple-50 dark:bg-purple-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>`
		},
		{
			id: 'audio',
			title: '语音与音乐',
			description: '将文本转为拟真语音，或进行音乐旋律创作。',
			prompt: '把下面的段落转换成温柔的女声配音：',
			color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/></svg>`
		},
		{
			id: 'realtime',
			title: '实时交互',
			description: '支持毫秒级低延迟的音视频实时交互与双向沟通。',
			prompt: '开启实时语音交互，我想和你练口语',
			color: 'text-indigo-500 bg-indigo-50 dark:bg-indigo-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>`
		}
	];

	const agentCards = [
		{
			id: 'writer',
			title: '写作助手',
			description: '精修文章、撰写文案，提升你的文字表达力。',
			prompt: '帮我把这段话润色得更专业、更有说服力：',
			color: 'text-pink-500 bg-pink-50 dark:bg-pink-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>`
		},
		{
			id: 'translator',
			title: '翻译官',
			description: '多语言互译，支持专业术语库与自然语气转换。',
			prompt: '请将以下段落翻译成地道的英文，保持专业语气：',
			color: 'text-cyan-500 bg-cyan-50 dark:bg-cyan-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5c-.347 2.225-1.517 4.542-3.13 6.368m-1.348-3.057A18.022 18.022 0 013 9.752"/></svg>`
		},
		{
			id: 'analyst',
			title: '数据分析师',
			description: '解析复杂数据，绘制分析表，并提炼核心洞察。',
			prompt: '如何对一个包含用户消费频次的数据集进行 RFM 聚类分析？',
			color: 'text-teal-500 bg-teal-50 dark:bg-teal-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`
		},
		{
			id: 'planner',
			title: '创意策划',
			description: '头脑风暴，策划品牌活动、视频脚本与创意文案。',
			prompt: '为一款面向年轻人的健康代餐奶昔策划一个趣味抖音短视频脚本',
			color: 'text-violet-500 bg-violet-50 dark:bg-violet-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>`
		},
		{
			id: 'coach',
			title: '心理导师',
			description: '倾听你的烦恼，提供温暖的心理疏导与自我成长建议。',
			prompt: '最近工作压力很大，总是失眠，有什么调节的建议吗？',
			color: 'text-orange-500 bg-orange-50 dark:bg-orange-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>`
		},
		{
			id: 'qa',
			title: '百科问答',
			description: '快速检索，回答科学、历史、常识等各类事实性问题。',
			prompt: '解释一下量子纠缠的基本原理，用通俗易懂的语言。',
			color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950/20',
			icon: `<svg class="size-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
		}
	];

	function handleCardClick(card) {
		onSelect({ type: 'prompt', data: card.prompt });
	}

	function focusInput() {
		// Dispatch key event or find elements to focus
		const inputEl = document.getElementById('chat-input');
		if (inputEl) {
			inputEl.focus();
		}
	}
</script>

<div class="m-auto w-full max-w-6xl px-4 md:px-8 py-10 flex flex-col justify-center items-center text-center">
	{#if $temporaryChatEnabled}
		<Tooltip
			content={$i18n.t("This chat won't appear in history and your messages will not be saved.")}
			className="w-full flex justify-center mb-4"
			placement="top"
		>
			<div class="flex items-center gap-2 text-gray-500 text-sm py-1 px-3 bg-gray-100 dark:bg-gray-800 rounded-full w-fit">
				<EyeSlash strokeWidth="2.5" className="size-3.5" />{$i18n.t('Temporary Chat')}
			</div>
		</Tooltip>
	{/if}

	<!-- Title Area -->
	<div class="flex flex-col items-center mb-8">
		<h1 class="text-3xl font-semibold tracking-tight text-gray-900 dark:text-gray-100 flex items-center gap-2">
			{$i18n.t('Explore Lingrai')}
			{#if activeTab === 'models'}
				<span class="text-blue-600 dark:text-blue-400">{$i18n.t('Models')}</span>
			{:else}
				<span class="text-purple-600 dark:text-purple-400">{$i18n.t('Agents')}</span>
			{/if}
		</h1>
		<p class="text-sm text-gray-500 dark:text-gray-400 mt-2 max-w-md">
			{#if activeTab === 'models'}
				{$i18n.t('Discover customized templates and flagship models tailored for your tasks.')}
			{:else}
				{$i18n.t('Deploy and chat with dedicated specialized agents for instant automation.')}
			{/if}
		</p>
	</div>

	<!-- Tab Switcher (Google AI Studio style) -->
	<div class="inline-flex rounded-full p-1 bg-gray-100 dark:bg-gray-800/80 mb-10 border border-gray-200/50 dark:border-gray-700/50">
		<button
			class="px-6 py-2 rounded-full text-sm font-medium transition-all duration-200 {activeTab === 'models' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 hover:text-gray-900 dark:hover:text-white'}"
			on:click={() => (activeTab = 'models')}
		>
			{$i18n.t('Models')}
		</button>
		<button
			class="px-6 py-2 rounded-full text-sm font-medium transition-all duration-200 {activeTab === 'agents' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 hover:text-gray-900 dark:hover:text-white'}"
			on:click={() => (activeTab = 'agents')}
		>
			{$i18n.t('Agents')}
		</button>
	</div>

	<!-- Active Model Header info if selectedModels is populated -->
	{#if models[selectedModelIdx]?.name}
		<div class="flex items-center gap-2 mb-6 px-3 py-1.5 bg-gray-50 dark:bg-gray-800/40 rounded-xl border border-gray-200/40 dark:border-gray-700/30 text-xs text-gray-500 dark:text-gray-400">
			<img
				src={`${WEBUI_API_BASE_URL}/models/model/profile/image?id=${models[selectedModelIdx]?.id}&lang=${$i18n.language}`}
				class="size-4.5 rounded-full"
				on:error={(e) => (e.currentTarget.src = '/favicon.png')}
				alt=""
			/>
			<span>{$i18n.t('Active Model')}: <strong>{models[selectedModelIdx]?.name}</strong></span>
		</div>
	{/if}

	<!-- Explorer Grid -->
	<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 w-full max-w-5xl">
		{#if activeTab === 'models'}
			{#each modelCards as card (card.id)}
				<button
					class="flex flex-col items-start text-left p-6 bg-white dark:bg-gray-800/30 rounded-2xl border border-gray-200/70 dark:border-gray-700/40 hover:border-blue-500/40 dark:hover:border-blue-400/40 hover:bg-blue-50/5 dark:hover:bg-blue-950/5 hover:shadow-lg hover:shadow-gray-200/10 hover:scale-[1.015] active:scale-[0.99] transition-all duration-200 group cursor-pointer"
					on:click={() => handleCardClick(card)}
				>
					<div class="p-3 rounded-xl mb-4 transition-colors {card.color}">
						{@html card.icon}
					</div>
					<h3 class="text-base font-semibold text-gray-800 dark:text-gray-200 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
						{$i18n.t(card.title)}
					</h3>
					<p class="text-xs text-gray-500 dark:text-gray-400 mt-2 leading-relaxed">
						{$i18n.t(card.description)}
					</p>
				</button>
			{/each}
		{:else}
			{#each agentCards as card (card.id)}
				<button
					class="flex flex-col items-start text-left p-6 bg-white dark:bg-gray-800/30 rounded-2xl border border-gray-200/70 dark:border-gray-700/40 hover:border-purple-500/40 dark:hover:border-purple-400/40 hover:bg-purple-50/5 dark:hover:bg-purple-950/5 hover:shadow-lg hover:shadow-gray-200/10 hover:scale-[1.015] active:scale-[0.99] transition-all duration-200 group cursor-pointer"
					on:click={() => handleCardClick(card)}
				>
					<div class="p-3 rounded-xl mb-4 transition-colors {card.color}">
						{@html card.icon}
					</div>
					<h3 class="text-base font-semibold text-gray-800 dark:text-gray-200 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
						{$i18n.t(card.title)}
					</h3>
					<p class="text-xs text-gray-500 dark:text-gray-400 mt-2 leading-relaxed">
						{$i18n.t(card.description)}
					</p>
				</button>
			{/each}
		{/if}
	</div>

	<!-- Start building Link -->
	<button
		on:click={focusInput}
		class="mt-10 inline-flex items-center gap-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 transition-colors cursor-pointer group"
	>
		<span>{$i18n.t('Start building')}</span>
		<svg class="size-4 transform group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
		</svg>
	</button>
</div>
